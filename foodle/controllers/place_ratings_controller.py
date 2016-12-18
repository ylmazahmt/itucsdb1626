#!/usr/bin/env python3
import foodle
import psycopg2
import re
import jwt
from psycopg2.extras import RealDictCursor, DictCursor
from foodle.utils.auth_hook import auth_hook_functor
from flask import Blueprint, render_template, redirect, current_app, request, make_response, g

import bcrypt

place_ratings_controller = Blueprint('place_ratings_controller', __name__)

@place_ratings_controller.route('/', methods=['GET'])
@auth_hook_functor
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 0

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT pr.id, u.username, pr.place_id, p.name, pr.rating
            FROM place_ratings AS pr
            INNER JOIN users AS u ON pr.user_id = u.id
            INNER JOIN places AS p ON pr.place_id = p.id
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            place_ratings = curs.fetchall()

            curs.execute(
            """
            SELECT count(id)
            FROM place_ratings
            """)

            count = curs.fetchone()[0]

            return render_template('/place_ratings/index.html', place_ratings=place_ratings, count=count)


@place_ratings_controller.route('/<int:id>', methods=['GET'])
@auth_hook_functor
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM place_ratings
            WHERE id = %s
            """,
            [id])

            place_rating = curs.fetchone()
            if place_rating is not None:
                return render_template('/place_ratings/show.html', place_rating=place_rating)
            else:
                return "Entity not found.", 404


@place_ratings_controller.route('/', methods=['POST'])
@auth_hook_functor
def create():
    user_id = int(request.json['user_id'])
    place_id = int(request.json['place_id'])
    rating = int(request.json['rating'])

    if not isinstance(rating, int) or not isinstance(user_id, int):
        return "Request rating is unprocessable", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO place_ratings
            (user_id, place_id, rating)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            [user_id, place_id, rating])

            place_rating = curs.fetchone()

            resp = make_response()
            resp.headers['location'] = '/place_ratings/' + str(place_rating['id'])

            return resp, 201


@place_ratings_controller.route('/new', methods=['GET'])
@auth_hook_functor
def new():
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT id, username, inserted_at
            FROM users
            """,
            )

            users = curs.fetchall()

            curs.execute(
            """
            SELECT id,name
            FROM places 
            """,
            )

            places = curs.fetchall()

    return render_template('/place_ratings/new.html', users = users, places = places)


@place_ratings_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
@auth_hook_functor
def update(id):
    rating = int(request.json['rating'])
    if request.json.get('id') is not None or not isinstance(rating, int):
        return "Request is unprocessable.", 422
    

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE place_ratings
            SET rating = %s 
            WHERE id = %s
            """, 
            [rating, id])

            if curs.rowcount is not 0:
                resp = make_response()
                resp.headers['location'] = '/place_ratings/' + str(id)

                return resp, 200
            else:
                return "Entity not found.", 404


@place_ratings_controller.route('/<int:id>/edit', methods=['GET'])
@auth_hook_functor
def edit(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM place_ratings
            WHERE id = %s
            """,
            [id])

            place_rating = curs.fetchone()

            if place_rating is not None:
                return render_template('/place_ratings/edit.html', place_rating=place_rating)
            else:
                return "Entity not found.", 404


@place_ratings_controller.route('/<int:id>', methods=['DELETE'])
@auth_hook_functor
def delete(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM place_ratings
            WHERE id = %s
            """,
            [id])

            if curs.rowcount is not 0:
                return "", 204
            else:
                return "Entity not found.", 404
