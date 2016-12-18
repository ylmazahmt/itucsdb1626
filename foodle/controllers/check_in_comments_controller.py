#!/usr/bin/env python3
import foodle
import psycopg2
import re
import jwt
from psycopg2.extras import RealDictCursor, DictCursor
from foodle.utils.auth_hook import auth_hook_functor
from flask import Blueprint, render_template, redirect, current_app, request, make_response, g

import bcrypt


check_in_comments_controller = Blueprint('check_in_comments_controller', __name__)

@check_in_comments_controller.route('/', methods=['GET'])
@auth_hook_functor
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 0

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT cic.id, u.username, cic.check_in_id, cic.body
            FROM check_in_comments AS cic
            INNER JOIN users AS u ON cic.user_id = u.id
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            check_in_comments = curs.fetchall()

            curs.execute(
            """
            SELECT count(id)
            FROM check_in_comments
            """)

            count = curs.fetchone()[0]

            return render_template('/check_in_comments/index.html', check_in_comments=check_in_comments, count=count)


@check_in_comments_controller.route('/<int:id>', methods=['GET'])
@auth_hook_functor
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM check_in_comments
            WHERE id = %s
            """,
            [id])

            check_in_comment = curs.fetchone()
            if check_in_comment is not None:
                return render_template('/check_in_comments/show.html', check_in_comment=check_in_comment)
            else:
                return "Entity not found.", 404


@check_in_comments_controller.route('/', methods=['POST'])
@auth_hook_functor
def create():
    user_id = int(request.json['user_id'])
    check_in_id = int(request.json['check_in_id'])
    body = request.json['body']

    if not isinstance(body, str) or not isinstance(user_id, int):
        return "Request body is unprocessable", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO check_in_comments
            (user_id, check_in_id, body)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            [user_id, check_in_id, body])

            check_in_comment = curs.fetchone()

            resp = make_response()
            resp.headers['location'] = '/check_in_comments/' + str(check_in_comment['id'])

            return resp, 201


@check_in_comments_controller.route('/new', methods=['GET'])
@auth_hook_functor
def new():
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT id, username, inserted_at
            FROM users
            """,
            )

            users = curs.fetchall()

            curs.execute(
            """
            SELECT ci.id, u.display_name, p.name
            FROM check_ins AS ci 
            INNER JOIN users AS u ON ci.user_id = u.id
            INNER JOIN places AS p ON ci.place_id = p.id
            """,
            )

            check_ins = curs.fetchall()

    return render_template('/check_in_comments/new.html', users = users, check_ins = check_ins)


@check_in_comments_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
@auth_hook_functor
def update(id):
    if request.json.get('id') is not None or not isinstance(request.json.get('body'), str):
        return "Request is unprocessable.", 422

    request.json['id'] = id

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE check_in_comments
            SET body = %(body)s
            WHERE id = %(id)s
            """, request.json)

            if curs.rowcount is not 0:
                resp = make_response()
                resp.headers['location'] = '/check_in_comments/' + str(id)

                return resp, 200
            else:
                return "Entity not found.", 404


@check_in_comments_controller.route('/<int:id>/edit', methods=['GET'])
@auth_hook_functor
def edit(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM check_in_comments
            WHERE id = %s
            """,
            [id])

            check_in_comment = curs.fetchone()

            if check_in_comment is not None:
                return render_template('/check_in_comments/edit.html', check_in_comment=check_in_comment)
            else:
                return "Entity not found.", 404


@check_in_comments_controller.route('/<int:id>', methods=['DELETE'])
@auth_hook_functor
def delete(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM check_in_comments
            WHERE id = %s
            """,
            [id])

            if curs.rowcount is not 0:
                return "", 204
            else:
                return "Entity not found.", 404
