import foodle
import psycopg2
from psycopg2.extras import DictCursor

from flask import Blueprint, render_template, current_app, request

import bcrypt

users_controller = Blueprint('users_controller', __name__)

@users_controller.route('/', methods=['GET'])
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 20

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

            results = curs.fetchall()

            return render_template('/users/index.html', users=results)


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

            return render_template('/users/show.html', user=user)


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
