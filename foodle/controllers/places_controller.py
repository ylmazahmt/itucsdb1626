#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor, RealDictCursor
from flask import Blueprint, render_template, current_app, request, redirect, jsonify, make_response

places_controller = Blueprint('places_controller', __name__)

@places_controller.route('/', methods=['GET'])
def index():
        acceptType = request.headers.get('accept')
        limit = request.args.get('limit') or 20
        offset = request.args.get('offset') or 0
        name = request.args.get('name')

        if acceptType == 'application/json':
            with psycopg2.connect(foodle.app.config['dsn']) as conn:
                with conn.cursor(cursor_factory=DictCursor) as curs:
                    if name is not None:
                        curs.execute(
                        """
                        SELECT p.id, p.name, p.description
                        FROM places p
                        WHERE p.name ILIKE %s
                        LIMIT %s
                        OFFSET %s
                        """,
                        ['%' + name + '%', limit, offset])
                    else:
                        curs.execute(
                        """
                        SELECT *
                        FROM places p
                        LIMIT %s
                        OFFSET %s
                        """,
                        [limit, offset])

                    places = curs.fetchall()

                    return jsonify(places)
        else:
            with psycopg2.connect(foodle.app.config['dsn']) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as curs:
                    curs.execute(
                    """
                    SELECT p.name, p.id, p.description, u.username
                    FROM places as p
                    INNER JOIN users as u ON p.user_id=u.id
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
                    count = curs.fetchone()['count']

                    for place in places:
                        curs.execute(
                        """
                        SELECT *
                        FROM place_instances
                        WHERE place_id = %s
                        LIMIT 10
                        """,
                        [place['id']])

                        place['place_instances'] = curs.fetchall()

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

            curs.execute(
            """
            SELECT *
            FROM place_instances
            WHERE id = %s
            """,
            [id]
            )

            place_instances = curs.fetchall()

            if place is not None:
                return render_template('/places/show.html', place=place, place_instances=place_instances)
            else:
                return "Entity not found.", 404


@places_controller.route('/', methods=['POST'])
def create():
    user_id = int(request.json['user_id'])
    name =  request.json['name']
    description = request.json['description']

    if not isinstance(name, str) or not isinstance(description, str) or not isinstance(user_id, int):
        return "Request body is unprocessable.", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO places
            (name, description, user_id)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            [name, description, user_id]
            )

            place = curs.fetchone()
            resp = make_response()
            resp.headers['location'] = '/places/' + str(place['id'])

            return resp, 201


@places_controller.route('/new', methods=['GET'])
def new():
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT id, username
            FROM users
            """,
            )
            users = curs.fetchall()

            return render_template('/places/new.html',users=users)


@places_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    name = request.json['name']
    description = request.json['description']

    if request.json.get('id') is not None or not isinstance(name, str) or not isinstance(description, str):
        return "Request is unprocessable.", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE places
            SET name = %s , description = %s
            WHERE id = %s
            """,
            [name, description, id])

            if curs.rowcount is not 0:
                resp = make_response()
                resp.headers['location'] = '/places/' + str(id)

                return resp, 200
            else:
                return "Place not found.", 404


@places_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
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
                return render_template('/places/edit.html',place=place)
            else:
                return "Place not found.", 404


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
                return "", 204
            else:
                return "Place not found.", 404
