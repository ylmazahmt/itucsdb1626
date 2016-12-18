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
                SELECT u.id, u.username, u.display_name, ui.url
                FROM users u
                LEFT OUTER JOIN user_images ui ON u.id = ui.user_id
                WHERE u.display_name ILIKE %s OR
                      u.username ILIKE %s ESCAPE '='
                LIMIT 5
                """,
                ['%' + parameter + '%', '%' + parameter + '%'])

                users = curs.fetchall()

                if len(users) < 5:
                    remaining = 5 - len(users)

                    curs.execute(
                    """
                    SELECT p.name, p.description, pi.url, p.id
                    FROM places p
                    LEFT OUTER JOIN place_images pi ON p.id = pi.place_id
                    WHERE p.name ILIKE %s OR
                          p.description ILIKE %s ESCAPE '='
                    LIMIT %s
                    """,
                    ['%' + parameter + '%', '%' + parameter + '%', remaining])

                    places = curs.fetchall()

                    return jsonify([users, places])
                else:
                    return jsonify([users])
    else:
        return "Invalid request.", 422
