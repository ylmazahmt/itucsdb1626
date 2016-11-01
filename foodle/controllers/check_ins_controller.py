#!/usr/bin/env python3
import foodle
import psycopg2
from flask import Blueprint, render_template, current_app, request, make_response, redirect

check_ins_controller = Blueprint('check_ins_controller', __name__)

@check_ins_controller.route('/', methods=['GET'])
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 20

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM check_ins
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            check_ins = curs.fetchall()

            curs.execute(
            """
            SELECT count(id)
            FROM check_ins
            """)

            count = curs.fetchone()[0]

            return render_template('/check_ins/index.html', check_ins=check_ins, count=check_ins)


@check_ins_controller.route('/<int:id>', methods=['GET'])
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM check_ins
            WHERE id = %s
            """,
            [id])

            check_in = curs.fetchone()

            if check_in is not None:
                return render_template('/check_ins/show.html', check_in=check_in)
            else:
                return "Entity not found.", 404


@check_ins_controller.route('/', methods=['POST'])
def create():
    if not isinstance(request.json.get('user_id'), int) or not isinstance(request.json.get('place_id'), int):
        return "Request body is unprocessable.", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO check_ins
            (user_id, place_id)
            VALUES (%(user_id)s, %(place_id)s)
            RETURNING *
            """, request.json)

            if curs.rowcount is not 0:
                return render_template('/check_ins/show.html', check_in=curs.fetchone())
            else:
                return "Entity not found.", 404


@check_ins_controller.route('/new', methods=['GET'])
def new():
    return render_template('/check_ins/new.html')


@check_ins_controller.route('/<int:id>', methods=['DELETE'])
def delete(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM check_ins
            WHERE id = %s
            """, [id])

            if curs.rowcount is not 0:
                return redirect('/check_ins/index.html')
            else:
                return "Entity not found.", 404
