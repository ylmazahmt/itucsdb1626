import foodle
import psycopg2
from psycopg2.extras import DictCursor
from flask import Blueprint, render_template, current_app, request, redirect, make_response

place_instances_controller = Blueprint('place_instances_controller',__name__)

@place_instances_controller.route('/', methods=['GET'])
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 0

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory = DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM place_instances
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            place_instances = curs.fetchall()

            curs.execute(
            """
            SELECT count(id)
            FROM place_instances
            """
            )
            count = curs.fetchone()[0]

            return render_template('place_instances/index.html', place_instances=place_instances, count=count)

@place_instances_controller.route('/<int:id>',methods=['GET'])
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory = DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM place_instances
            WHERE id = %s
            """,
            [id]
            )

            place_instance = curs.fetchone()

            if place_instance is not None:
                return render_template('place_instances/show.html', place_instance=place_instance)
            else:
                return "Entity not found.",404


@place_instances_controller.route('/', methods=['POST'])
def create():
    name = request.json['name']
    capacity = request.json['capacity']
    user_id = request.json['user_id']
    place_id = request.json['place_id']

    if not isinstance(name, str) or not isinstance(capacity, str) or not isinstance(user_id, int) or not isinstance(place_id, int):
        return "Request body is unprocessable.", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO place_instances
            (name, user_id, place_id, capacity)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            [name, user_id, place_id, capacity]
            )
            place_instance = curs.fetchone()

            resp = make_response()
            resp.headers['location'] = '/place_instances/' + str(curs.fetchone()['id'])
            return resp, 201

@place_instances_controller.route('/new', methods=['GET'])
def new():
    return render_template('place_instances/new.html')

@place_instances_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):

    request.json['id'] = id

    if request.json.get('id') is not None or not isinstance(request.json.get('name'), str) or not isinstance(request.json.get('capacity'), str):
        return "Request body is unprocessable.", 422

        request.json['id']= id
        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                UPDATE place_instances
                SET name = %(name)s,
                    capacity = %(capacity)s
                WHERE id = %(id)s
                """, request.json
                )

                if curs.rowcount is not 0:
                    resp = make_response()
                    resp.headers['location'] = '/place_instances/' + str(id)
                    return resp, 200
                else:
                    return "Entity not found.", 404

@place_instances_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM place_instances
            WHERE id = %s
            """, [id]
            )
            place_instance = curs.fetchone()

            if place_instance is not None:
                return render_template ('/place_instances/edit.html', place_instance = place_instance)
            else:
                return "Entity not found.", 404

@place_instances_controller.route('/<int:id>', methods=['DELETE'])
def delete(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM place_instances
            WHERE id = %s
            """, [id]
            )

            if curs.rowcount is not 0:
                return "", 204
            else:
                return "Entity not found.", 404
