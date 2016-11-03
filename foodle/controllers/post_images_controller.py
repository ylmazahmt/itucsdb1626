#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor

from flask import Blueprint, render_template, current_app, request, make_response

post_images_controller = Blueprint('post_images_controller', __name__)


@post_images_controller.route('/', methods=['GET'])
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 0

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT pi.*
            FROM post_images AS pi
            LEFT JOIN ipv4_blacklist AS b ON pi.ip_addr = b.ip_addr
            WHERE b.id IS NULL
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])
            post_images = curs.fetchall()

            curs.execute(
            """
            SELECT count(pi.id)
            FROM post_images AS pi
            LEFT JOIN ipv4_blacklist AS b ON pi.ip_addr = b.ip_addr
            WHERE b.id IS NULL
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])
            post_image_count = curs.fetchone()

        return render_template('/post_images/index.html', post_images = post_images, post_image_count=post_image_count)


@post_images_controller.route('/<int:id>', methods=['GET'])
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT id, post_id, inserted_at, link
            FROM post_images
            WHERE id = %s
            """,
            [id])

            post_image = curs.fetchone()

            if post_image is not None:
                return render_template('/post_images/show.html', post_image=post_image)
            else:
                return "Entity not found.", 404


@post_images_controller.route('/', methods=['POST'])
def create():
    # print('hey')
    link = request.json.get('link')
    post_id = request.json.get('post_id')

    if not isinstance(link, str) and not isinstance(post_id, int):
        return "Request body is unprocessable.", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO post_images
            (link, post_id, ip_addr)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            [link, post_id, request.access_route[0]])

            post_image = curs.fetchone()

            resp = make_response()
            resp.headers['location'] = '/post_images/' + str(post_image['id'])

            return resp, 201


@post_images_controller.route('/new', methods=['GET'])
def new():
    return render_template('/post_images/new.html')


@post_images_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    link = request.json.get('link')

    request.json['id'] = id
    request.json['ip_addr'] = request.access_route[0]

    if not isinstance(link, str):
        return "Request body is unprocessable.", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE post_images
            SET link = %(link)s,
                ip_addr = %(ip_addr)s
            WHERE id = %(id)s
            """, request.json)

            if curs.rowcount is not 0:
                resp = make_response()
                resp.headers['location'] = '/post_images/' + str(id)

                return resp
            else:
                return "Entity not found.", 404


@post_images_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT id, post_id, link, inserted_at
            FROM post_images
            WHERE id = %s
            """,
            [id])

            post_image = curs.fetchone()

            if post_image is not None:
                return render_template('/post_images/edit.html', post_image=post_image)
            else:
                return "Entity not found.", 404


@post_images_controller.route('/<int:id>', methods=['DELETE'])
def delete(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM post_images
            WHERE id = %s
            """,
            [id])

            if curs.rowcount is 1:
                return "", 204
            else:
                return "Entity not found.", 404
