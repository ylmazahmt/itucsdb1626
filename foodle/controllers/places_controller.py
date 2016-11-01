#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor
from flask import Blueprint, render_template, current_app, request, redirect

places_controller = Blueprint('places_controller', __name__)

@places_controller.route('/', methods=['GET'])
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 20

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM places
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            places = curs.fetchall()

            curs.execute(
            """
            SELECT count(*)
            FROM places
            """)

            count = curs.fetchone()[0]

            return render_template('/places/index.html', places=places, count=count)


@places_controller.route('/<int:id>', methods=['GET'])
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM places
            WHERE id = %s
            """,
            [id])

            place = curs.fetchone()

            if place is not None:
                return render_template('/places/show.html', place=place)
            else:
                return "Entity not found.", 404


@places_controller.route('/', methods=['POST'])
def create():
    if not isinstance(request.json.get('name'), str) or not isinstance(request.json.get('description'), str) or not isinstance(request.json.get('user_id'), int):
        return "Request body is unprocessable.", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO places
            (name, description, user_id)
            VALUES (%(name)s, %(description)s, %(user_id)s)
            RETURNING *
            """, request.json)

            place = curs.fetchone()

            if place is not None:
                return render_template('/places/show.html', place=place)
            else:
                return "Entity not found.", 404


@places_controller.route('/new', methods=['GET'])
def new():
    return render_template('/places/new.html')


@places_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    if request.json.get('id') is not None or not isinstance(request.json.get('name'), str) or not isinstance(request.json.get('description'), str) or not isinstance(request.json.get('user_id'), int):
        return "Request body is unprocessable.", 422

    request.json['id'] = id

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE places
            SET name = %(name)s,
                description = %(description)s,
                user_id = %(user_id)s
            WHERE id = %(id)s
            RETURNING *
            """, request.json)

            if curs.rowcount is not 0:
                return render_template('/places/show.html', place=curs.fetchone())
            else:
                return "Entity not found.", 404


@places_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    return None

@places_controller.route('/<int:id>', methods=['DELETE'])
def delete(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM places
            WHERE id = %s
            """, [id])

            if curs.rowcount is not 0:
                return redirect('/places/index.html')
            else:
                return "Entity not found.", 404
