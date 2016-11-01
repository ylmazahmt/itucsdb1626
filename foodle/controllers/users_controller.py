#!/usr/bin/env python3
import foodle
import psycopg2
import re
from psycopg2.extras import DictCursor

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
            SELECT id, username, inserted_at
            FROM users
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
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT id, username, inserted_at
            FROM users
            WHERE id = %s
            """,
            [id])

            user = curs.fetchone()

            if user is not None:
                return render_template('/users/show.html', user=user)
            else:
                return "Entity not found.", 404


@users_controller.route('/', methods=['POST'])
def create():
    username = request.json['username']
    password = request.json['password']

    if not isinstance(username, str) or not isinstance(password, str):
        return "Request body is unprocessable.", 422

    pattern = re.compile("^([A-Z][a-z][0-9]{5-20})")

    if not pattern.match(password) or not pattern.match(username):
        return "Username and password should be alphanumeric and be 5 to 20 characters long.", 422

    password_digest = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO users
            (username, password_digest)
            VALUES (%s, %s)
            RETURNING *
            """,
            [username, password_digest])

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

    request.json['id'] = id

    if not isinstance(username, str) or not isinstance(password, str):
        return "Request body is unprocessable.", 422

    username_pattern = re.compile("[a-zA-Z0-9]{3,20}")
    password_pattern = re.compile("[a-zA-Z0-9]{7,20}")

    if not password_pattern.match(password) or not username_pattern.match(username):
        return "Username and password should be alphanumeric and be 5 to 20 characters long.", 422

    request.json['password_digest'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE users
            SET username = %(username)s,
                password_digest = %(password_digest)s
            WHERE id = %(id)s
            """, request.json)

            if curs.rowcount is not 0:
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
            SELECT id, username, inserted_at
            FROM users
            WHERE id = %s
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
