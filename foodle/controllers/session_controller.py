#!/usr/bin/env python3
import foodle
import psycopg2
import jwt
from flask import Blueprint, render_template, redirect, request, make_response, current_app
from psycopg2.extras import RealDictCursor
from bcrypt import checkpw

session_controller = Blueprint('session_controller', __name__)

@session_controller.route('/new', methods=['GET'])
def new():
    return render_template('/sessions/new.html')

@session_controller.route('/', methods=['POST'])
def create():
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
            """
            SELECT u.id, u.username, u.password_digest, u.inserted_at, u.display_name
            FROM users u
            WHERE u.username = %s
            LIMIT 1
            """,
            [request.json['username']])

            if curs.rowcount == 1:
                user = curs.fetchone()

                if (checkpw(request.json['password'].encode('utf-8'), user['password_digest'].encode('utf-8'))):
                    resp = make_response()

                    user['inserted_at'] = user['inserted_at'].isoformat()

                    token = jwt.encode(user, current_app.secret_key, algorithm='HS256')
                    resp.set_cookie('jwt', value=token)
                    resp.headers['location'] = '/users/' + str(user['id']) + '/feed'

                    return resp, 201
                else:
                    return "Not found", 404
            else:
                return "Not found", 404

    return None
