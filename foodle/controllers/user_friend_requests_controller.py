#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor

from flask import Blueprint, render_template, redirect, current_app, request, make_response

import bcrypt

user_friend_requests_controller = Blueprint('user_friend_requests_controller', __name__)

@user_friend_requests_controller.route('/<int:id>/friend_requests', methods=['GET'])
def index(id):
	limit = request.args.get('limit') or 20
	offset = request.args.get('offset') or 0

	with psycopg2.connect(foodle.app.config['dsn']) as conn:
		with conn.cursor(cursor_factory=DictCursor) as curs:
			curs.execute(
			"""
        	SELECT u.id, u.username, u.display_name, ui.url, u.inserted_at
        	FROM user_friends AS uf
        	INNER JOIN users AS u ON u.id = uf.user_id
        	INNER JOIN user_images AS ui ON ui.user_id = u.id
        	WHERE uf.friend_id = %s AND uf.is_friend = FALSE
        	LIMIT %s
        	OFFSET %s
        	""",
        	[id, limit, offset])

			requests = curs.fetchall()

			curs.execute(
			"""
			SELECT count(uf.id)
			FROM user_friends AS uf
			INNER JOIN users AS u ON u.id = uf.user_id
			WHERE uf.friend_id = %s AND uf.is_friend = FALSE
			""",
			[id])

			request_count = curs.fetchone()[0]

	return render_template('/users/friends/requests_index.html', requests = requests, request_count = request_count, current_user = id)


@user_friend_requests_controller.route('/<int:id>/friend_requests', methods=['POST'])
def accept_friend_request(id):
	second_user_id = request.form['user_to_get']
	with psycopg2.connect(foodle.app.config['dsn']) as conn:
		with conn.cursor(cursor_factory=DictCursor) as curs:
			curs.execute(
			"""
			INSERT INTO user_friends
			(user_id, friend_id, is_friend)
			VALUES(%s, %s, True)
			""",
			[id, second_user_id])

			curs.execute(
			"""
			UPDATE user_friends
			SET is_friend = True
			WHERE user_id = %s
			AND friend_id = %s
			""",
			[second_user_id, id])

	return redirect("users/"+ str(id) + "/friend_requests", code=302)
