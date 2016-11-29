#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor

from flask import Blueprint, render_template, current_app, request

user_user_activation_controller = Blueprint('user_user_activation_controller', __name__)

@user_user_activation_controller.route('/users/<int:user_id>/user_activation', methods=['GET'])
def show(user_id):
    #   TODO: Side-join table with users and exclusive check of entity
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM user_activation
            WHERE user_id = %s
            """,
            [user_id])

            result = curs.fetchone()

            if results is not None:
                return render_template('/users/user_activation/show.html', user_activation=result)
            else:
                return "Entity not found.", 404


@user_user_activation_controller.route('/users/<int:user_id>/user_activation', methods=['POST'])
def create(user_id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("BEGIN")

            curs.execute(
            """
            SELECT activation_key
            FROM users u
            WHERE u.id = %s
            """,
            [user_id])

            activation_key = curs.fetchone()[0]

            print(request.json.get('activation_key'))
            print(activation_key)

            if request.json.get('activation_key') == activation_key:
                curs.execute(
                """
                INSERT INTO user_activations
                (user_id)
                VALUES (%s)
                """,
                [user_id])

                rowCount = curs.rowcount

                curs.execute("COMMIT")

                if rowCount is not 0:
                    return "User activated.", 201
                else:
                    return "Entity not found.", 404
            else:
                curs.execute("ROLLBACK")

                return "Wrong activation key.", 405


@user_user_activation_controller.route('/users/<int:user_id>/user_activation/new', methods=['GET'])
def new(user_id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT id, display_name, activation_key
            FROM users
            WHERE id = %s
            """,
            [user_id])

            user = curs.fetchone()

            if user is not None:
                return render_template('/users/user_activation/new.html', user=user)
            else:
                return "Entity not found.", 404
