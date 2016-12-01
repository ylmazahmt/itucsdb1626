#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor

from flask import Blueprint, render_template, current_app, request, make_response

import bcrypt


user_friends_controller = Blueprint('user_friends_controller', __name__)

@user_friends_controller.route('/<int:id>/friends/', methods=['GET'])
def index(id):
	limit = request.args.get('limit') or 20
	offset = request.args.get('offset') or 0

	with psycopg2.connect(foodle.app.config['dsn']) as conn:
		with conn.cursor(cursor_factory=DictCursor) as curs:
			curs.execute(
			"""
			SELECT u.id, u.username, u.display_name, ui.url, u.inserted_at
        	FROM user_friends AS uf
        	INNER JOIN users AS u ON u.id = uf.friend_id
        	INNER JOIN user_images AS ui ON ui.user_id = u.id
        	WHERE uf.user_id = %s
        	AND uf.is_friend = TRUE
        	LIMIT %s
        	OFFSET %s
        	""",
        	[id, limit, offset])
			friends = curs.fetchall()

			curs.execute(
			"""
			SELECT count(uf.id)
        	FROM user_friends AS uf
        	INNER JOIN users AS u ON u.id = uf.friend_id
        	WHERE uf.user_id = %s
        	AND uf.is_friend = TRUE
        	""",
        	[id])

			friend_count = curs.fetchone()[0]

	return render_template('/users/friends/index.html', friends = friends, friend_count = friend_count)

@user_friends_controller.route('/<int:id>/friends/', methods=['POST'])
def remove(id):
	second_user_id = request.form['user_to_get']
	with psycopg2.connect(foodle.app.config['dsn']) as conn:
		with conn.cursor(cursor_factory=DictCursor) as curs:
			curs.execute(
			"""
			DELETE FROM user_friends
        	WHERE (user_id = %s
        	AND friend_id = %s
        	AND is_friend)
        	OR (user_id = %s
        	AND friend_id = %s
        	AND is_friend)
        	""",
        	[id, second_user_id, second_user_id, id])

	return render_template('/users/friends/index.html')

@user_friends_controller.route('/<int:id>/friends/search', methods=['POST'])
def search(id):
	limit = request.args.get('limit') or 20
	offset = request.args.get('offset') or 0

	string_to_search = request.form['search_friend']

	with psycopg2.connect(foodle.app.config['dsn']) as conn:
		with conn.cursor(cursor_factory=DictCursor) as curs:
			curs.execute(
			"""
			SELECT u.id, u.username, u.display_name, ui.url, u.inserted_at
        	FROM user_friends AS uf
        	INNER JOIN users AS u ON u.id = uf.friend_id
        	INNER JOIN user_images AS ui ON ui.user_id = u.id
        	WHERE uf.user_id = %s
        	AND u.display_name ILIKE %s OR u.username ILIKE %s ESCAPE '='
        	AND uf.is_friend 
        	LIMIT %s
        	OFFSET %s
        	""",
        	[id,'%' + string_to_search + '%', '%' + string_to_search + '%', limit, offset])

			friends = curs.fetchall()

	return render_template('/users/friends/index.html', friends = friends)

@user_friends_controller.route('/<int:id>/friends/new_friend', methods=['GET'])
def new_friend(id):
        limit = request.args.get('limit') or 20
        offset = request.args.get('offset') or 0

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
                with conn.cursor(cursor_factory=DictCursor) as curs:
                        curs.execute(
                        """
                        SELECT u.id, u.username, u.display_name, u.inserted_at, ui.url
                        FROM users u
                        LEFT OUTER JOIN user_images ui ON u.id = ui.user_id
                        LIMIT %s
                        OFFSET %s
                        """,
                        [limit, offset])

                        users = curs.fetchall()

        return render_template('/users/friends/new_friend.html', users = users, current_user = id)