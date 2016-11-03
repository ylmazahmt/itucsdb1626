#!/usr/bin/env python3
import foodle
import psycopg2
import re
from psycopg2.extras import DictCursor

from flask import Blueprint, render_template, current_app, request, make_response

import bcrypt

blacklist_controller = Blueprint('blacklist_controller', __name__)

@blacklist_controller.route('/', methods=['POST'])
def create():
    ip_addr = request.json.get('ip_addr')
    salt = request.json.get('salt')

    if bcrypt.checkpw(salt.encode('utf-8'), '$2b$14$xO/qNk0bzQk4A3BBGHRU6eL5d88xvL2F/vuZX2D9aneuO9YTQMRuO'.encode('utf-8')):
        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                INSERT INTO ipv4_blacklist
                (ip_addr)
                VALUES (%s)
                RETURNING *
                """,
                [ip_addr])

                if curs.rowcount is not 0:
                    return "201", 201
                else:
                    raise "Server error."
    else:
        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                INSERT INTO ipv4_blacklist
                (ip_addr)
                VALUES (%s)
                RETURNING *
                """,
                [request.access_route[0]])

                return "I'm a teapot.", 418
