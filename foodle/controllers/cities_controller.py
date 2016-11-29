#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor,RealDictCursor

from flask import Blueprint, render_template, current_app, request, make_response

cities_controller = Blueprint('cities_controller',__name__)

@cities_controller.route('/',methods=['GET'])
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 0

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
            """
            SELECT c.id, c.name, c.description, u.username
            FROM cities as c
            INNER JOIN users as u ON c.user_id=u.id
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            cities = curs.fetchall()

            curs.execute(
            """
            SELECT count(id)
            FROM cities
            """)

            count = curs.fetchone()['count']

            for city in cities:
                curs.execute(
                """
                SELECT *
                FROM place_instances
                WHERE city_id = %s
                LIMIT 10
                """,
                [city['id']])

                city['place_instances'] = curs.fetchall()


            return render_template('/cities/index.html', cities=cities,count=count)

@cities_controller.route('/<int:id>', methods=['GET'])
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT id, name, description
            FROM cities
            WHERE id = %s
            """,
            [id])

            city = curs.fetchone()

            curs.execute(
            """
            SELECT *
            FROM place_instances
            WHERE city_id = %s
            """,
            [id]
            )
            place_instances = curs.fetchall()

            if city is not None:
                return render_template('/cities/show.html', city=city,place_instances=place_instances)
            else:
                return "City not found.", 404

@cities_controller.route('/',methods=['POST'])
def create():
    user_id = int(request.json['user_id'])
    name =  request.json['name']
    description = request.json['description']

    if not isinstance(user_id,int) or not isinstance(name,str) or not isinstance(description,str):
        return "Request rating is unprocessable",422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO cities
            (user_id, name, description)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            [user_id, name, description])

            city=curs.fetchone()
            resp = make_response()
            resp.headers['location'] = '/cities/' + str(city['id'])

            return resp, 201

@cities_controller.route('/new', methods=['GET'])
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

            return render_template('/cities/new.html',users=users)

@cities_controller.route('/<int:id>', methods=['PUT','PATCH'])
def update(id):
    name = request.json['name']
    description = request.json['description']

    if request.json.get('id') is not None or not isinstance(name, str) or not isinstance(description, str):
        return "Request is unprocessable.", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE cities
            SET name = %s , description = %s
            WHERE id = %s
            """,
            [name, description, id])

            if curs.rowcount is not 0:
                resp = make_response()
                resp.headers['location'] = '/cities/' + str(id)

                return resp, 200
            else:
                return "City not found.", 404

@cities_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM cities
            WHERE id = %s
            """,
            [id])

            city = curs.fetchone()

            if city is not None:
                return render_template('/cities/edit.html',city=city)
            else:
                return "City not found.", 404

@cities_controller.route('/<int:id>',methods=['DELETE'])
def delete(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM cities
            WHERE id = %s
            """,
            [id])
            if curs.rowcount is not 0:
                return "",204
            else:
                return "City not found.",404
