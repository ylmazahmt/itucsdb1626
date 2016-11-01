import foodle
import psycopg2
from psycopg2.extras import DictCursor

from flask import Blueprint, render_template, current_app

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
            curs.execute(
            """
            INSERT INTO user_activations
            (user_id)
            VALUES user_id = %s
            """,
            [user_id])

            result = curs.fetchone()

            if results is not None:
                return render_template('/users/user_activation/show.html', user_activation=result)
            else:
                return "Entity not found.", 404
