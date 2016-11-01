#!/usr/bin/env python3
import foodle
import psycopg2
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

    if len(username) < 5 or len(username) > 20:
        return "Username should have length between 5 and 20.", 422

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

            print(curs.fetchone())

            return "", 204
