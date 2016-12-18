#!/usr/bin/env python3
import foodle
from flask import Blueprint, render_template, current_app, request, jsonify, g
import psycopg2
from psycopg2.extras import RealDictCursor, DictCursor
from foodle.utils.auth_hook import auth_hook_functor

like_controller = Blueprint('like_controller', __name__)

@like_controller.route('/posts/<int:post_id>/like', methods=['GET'])
@auth_hook_functor
def show(post_id):
    user_id = g.current_user['id']

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
            """
            SELECT u.id, p.id, pl.*
            FROM post_likes pl
            RIGHT OUTER JOIN users u ON u.id = pl.user_id
            RIGHT OUTER JOIN posts p ON p.id = pl.post_id
            WHERE u.id = %s AND
                  p.id = %s
            """,
            [user_id, post_id])

            like = curs.fetchone()

            if not like is None:
                return jsonify(like)
            else:
                return "Like not found", 404

@like_controller.route('/posts/<int:post_id>/like', methods=['POST'])
@auth_hook_functor
def create(post_id):
    user_id = g.current_user['id']

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
            """
            INSERT INTO post_likes
            (post_id, user_id)
            VALUES (%s, %s)
            RETURNING *
            """,
            [post_id, user_id])

            like = curs.fetchone()
            if not like is None:
                return jsonify(like)
            else:
                return 404


@like_controller.route('/posts/<int:post_id>/like', methods=['DELETE'])
@auth_hook_functor
def delete(post_id):
    user_id = g.current_user['id']

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
            """
            DELETE FROM post_likes
            WHERE post_id = %s AND
                  user_id = %s
            """,
            [post_id, user_id])

            if curs.rowcount is 1:
                return "", 204
            else:
                return "Like not found.", 404
