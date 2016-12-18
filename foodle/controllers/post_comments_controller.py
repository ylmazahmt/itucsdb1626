#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor
from flask import Blueprint, render_template, current_app, request, redirect, make_response, g
from foodle.utils.auth_hook import auth_hook_functor

post_comments_controller = Blueprint('post_comments_controller', __name__)

@post_comments_controller.route('/', methods=['GET'])
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 0

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT pc.id, u.username, pc.post_id, pc.body
            FROM post_comments AS pc
            INNER JOIN users AS u ON pc.user_id = u.id
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            post_comments = curs.fetchall()

            curs.execute(
            """
            SELECT count(id)
            FROM post_comments
            """)

            count = curs.fetchone()[0]

            return render_template('/post_comments/index.html', post_comments=post_comments, count=count)


@post_comments_controller.route('/<int:id>', methods=['GET'])
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM post_comments
            WHERE id = %s
            """,
            [id])

            post_comment = curs.fetchone()

            if post_comment is not None:
                return render_template('/post_comments/show.html', post_comment=post_comment)
            else:
                return "Entity not found.", 404


@post_comments_controller.route('/<int:post_id>/comments/', methods=['POST'])
@auth_hook_functor
def create(post_id):
    user_id = g.current_user['id']
    body = request.json['body']

    if not isinstance(body, str) or not isinstance(user_id, int):
        return "Request body is unprocessable", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO post_comments
            (user_id, post_id, body)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            [user_id, post_id, body])

            post_comment = curs.fetchone()

            resp = make_response()
            resp.headers['location'] = '/post_comments/' + str(post_comment['id'])

            return resp, 201


@post_comments_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    if request.json.get('id') is not None or not isinstance(request.json.get('body'), str):
        return "Request is unprocessable.", 422

    request.json['id'] = id

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE post_comments
            SET body = %(body)s
            WHERE id = %(id)s
            """, request.json)

            if curs.rowcount is not 0:
                resp = make_response()
                resp.headers['location'] = '/post_comments/' + str(id)

                return resp, 200
            else:
                return "Entity not found.", 404


@post_comments_controller.route('/<int:post_id>/comments/<int:id>/', methods=['DELETE'])
def delete(post_id, id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM post_comments
            WHERE id = %s
            """,
            [id])

            if curs.rowcount is not 0:
                return "", 204
            else:
                return "Entity not found.", 404
