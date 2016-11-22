#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor

from flask import Blueprint, render_template, current_app, request, make_response, jsonify

search_controller = Blueprint('search_controller', __name__)

@search_controller.route('/', methods=['GET'])
def index():
    parameter = request.args.get('parameter')

    if parameter is not None:
        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                SELECT u.username, u.display_name
                FROM users u
                WHERE u.display_name LIKE %s OR
                      u.username LIKE %s ESCAPE '='
                LIMIT 5
                """,
                ['%' + parameter + '%', '%' + parameter + '%'])

                users = curs.fetchall()

                if len(users) < 5:
                    remaining = 5 - len(users)

                    curs.execute(
                    """
                    SELECT p.name, p.description
                    FROM places p
                    WHERE p.name LIKE %s OR
                          p.description LIKE %s ESCAPE '='
                    LIMIT %s
                    """,
                    ['%' + parameter + '%', '%' + parameter + '%', remaining])

                    places = curs.fetchall()

                    return jsonify([*users, *places])
                else:
                    return jsonify([*users])
    else:
        return "Invalid request.", 422
