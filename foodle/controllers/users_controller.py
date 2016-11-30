#!/usr/bin/env python3
import foodle
import psycopg2
import re
from psycopg2.extras import RealDictCursor, DictCursor

from flask import Blueprint, render_template, current_app, request, make_response

import bcrypt

users_controller = Blueprint('users_controller', __name__)

@users_controller.route('/', methods=['GET'])
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 0

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT u.id, u.username, u.display_name, u.inserted_at, ui.url
            FROM users u
            LEFT OUTER JOIN user_images ui ON u.id = ui.user_id
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            users = curs.fetchall()

            curs.execute(
            """
            SELECT count(id)
            FROM users
            """)

            count = curs.fetchone()[0]

            return render_template('/users/index.html', users=users, count=count)


@users_controller.route('/<int:id>', methods=['GET'])
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
            """
            SELECT u.id,
                   u.username,
                   u.display_name,
                   count(uf.id) number_of_friends,
                   ui.url image_url,
                   max(p.inserted_at) last_posted,
                   count(p.id) number_of_posts,
                   ua.user_id IS NOT NULL is_activated
            FROM users u
            LEFT OUTER JOIN user_images ui ON ui.user_id = u.id
            LEFT OUTER JOIN user_friends uf ON uf.user_id = u.id AND uf.is_friend = True
            LEFT OUTER JOIN posts p ON p.user_id = u.id
            LEFT OUTER JOIN user_activations ua ON ua.user_id = u.id
            GROUP BY u.id, ui.user_id, ua.user_id
            HAVING u.id = %s;
            """,
            [id])

            user = curs.fetchone()

            curs.execute(
            """
            SELECT f.*, pl.user_id IS NOT NULL is_liked
            FROM feed f
            LEFT OUTER JOIN post_likes pl ON (f.post_id = pl.post_id AND pl.user_id = %s)
            WHERE f.user_id = %s
            """,
            [2, id])

            feeds = curs.fetchall()

            for each_feed in feeds:
                curs.execute(
                """
                SELECT link
                FROM post_images
                WHERE post_id = %s
                LIMIT 5
                """,
                [each_feed['post_id']])

                each_feed['post_images'] = curs.fetchall()

            if user is not None:
                return render_template('/users/show.html', user=user, feeds=feeds)
            else:
                return "Entity not found.", 404


@users_controller.route('/', methods=['POST'])
def create():
    username = request.json.get('username')
    password = request.json.get('password')
    display_name = request.json.get('display_name')
    ip_address = request.access_route[0]

    if not isinstance(username, str) or not isinstance(password, str) or not isinstance(display_name, str):
        return "Request body is unprocessable.", 422

    username_pattern = re.compile("[a-zA-Z0-9]{3,20}")
    password_pattern = re.compile("[a-zA-Z0-9]{7,20}")

    if not password_pattern.match(password) or not username_pattern.match(username):
        return "Username and password should be alphanumeric and be 5 to 20 characters long.", 422

    password_digest = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO users
            (username, display_name, password_digest, ip_address)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            [username, display_name, password_digest, ip_address])

            user = curs.fetchone()

            resp = make_response()
            resp.headers['location'] = '/users/' + str(user['id'])

            return resp, 201


@users_controller.route('/new', methods=['GET'])
def new():
    return render_template('/users/new.html')


@users_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    username = request.json.get('username')
    password = request.json.get('password')
    user_image_url = request.json.get('user_image_url')

    request.json['id'] = id

    if password is not None:
        if not isinstance(username, str) or not isinstance(password, str):
            return "Request body is unprocessable.", 422

        request.json['password_digest'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                BEGIN
                """
                )

                print(user_image_url)

                if len(user_image_url) > 0:
                    curs.execute(
                    """
                    UPDATE user_images
                    SET url = %s
                    WHERE user_id = %s
                    """,
                    [user_image_url, id])

                    print(curs.rowcount)

                    if curs.rowcount == 0:
                        curs.execute(
                        """
                        INSERT INTO user_images
                        (user_id, url)
                        VALUES (%s, %s)
                        """,
                        [id, user_image_url])

                        print(curs.rowCount)

                curs.execute(
                """
                UPDATE users
                SET username = %(username)s,
                    password_digest = %(password_digest)s,
                    display_name = %(display_name)s
                WHERE id = %(id)s
                """, request.json)

                rowCount = curs.rowcount

                curs.execute(
                """
                COMMIT
                """
                )

                if rowCount is not 0:
                    resp = make_response()
                    resp.headers['location'] = '/users/' + str(id)

                    return resp
                else:
                    return "Entity not found.", 404
    else:
        if not isinstance(username, str):
            return "Request body is unprocessable.", 422

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                BEGIN
                """
                )

                if len(user_image_url) > 0:
                    curs.execute(
                    """
                    UPDATE user_images
                    SET url = %s
                    WHERE user_id = %s
                    """,
                    [user_image_url, id])

                    if curs.rowcount == 0:
                        curs.execute(
                        """
                        INSERT INTO user_images
                        (user_id, url)
                        VALUES (%s, %s)
                        """,
                        [id, user_image_url])

                curs.execute(
                """
                UPDATE users
                SET username = %(username)s,
                    display_name = %(display_name)s
                WHERE id = %(id)s
                """, request.json)

                rowCount = curs.rowcount

                curs.execute(
                """
                COMMIT
                """
                )

                if rowCount is not 0:
                    resp = make_response()
                    resp.headers['location'] = '/users/' + str(id)

                    return resp
                else:
                    return "Entity not found.", 404


@users_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT u.id,
                   u.username,
                   u.display_name,
                   count(uf.id) number_of_friends,
                   ui.url image_url,
                   max(p.inserted_at) last_posted,
                   count(p.id) number_of_posts
            FROM users u
            LEFT OUTER JOIN user_images ui ON ui.user_id = u.id
            LEFT OUTER JOIN user_friends uf ON uf.user_id = u.id
            LEFT OUTER JOIN posts p ON p.user_id = u.id
            GROUP BY u.id, ui.user_id
            HAVING u.id = %s;
            """,
            [id])

            user = curs.fetchone()

            if user is not None:
                return render_template('/users/edit.html', user=user)
            else:
                return "Entity not found.", 404


@users_controller.route('/<int:id>', methods=['DELETE'])
def delete(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM users
            WHERE id = %s
            """,
            [id])

            if curs.rowcount is 1:
                return "", 204
            else:
                return "Entity not found.", 404
