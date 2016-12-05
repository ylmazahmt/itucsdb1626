#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor

from flask import Blueprint, render_template, redirect, current_app, request, make_response

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

			curs.execute(
			"""
			SELECT u.id, count(u.id) prc, u.username, u.display_name, ui.url, u.inserted_at
			FROM user_friends AS uf
			INNER JOIN users AS u ON u.id = uf.friend_id
			INNER JOIN user_images AS ui ON ui.user_id = u.id
			WHERE uf.user_id = %s
			AND uf.is_friend = FALSE
			GROUP BY u.id, ui.url
			""",
			[id])

			pending_requests = curs.fetchall()

			curs.execute(
			"""
			SELECT count(u.id)
			FROM user_friends AS uf
			INNER JOIN users AS u ON u.id = uf.friend_id
			WHERE uf.user_id = %s
			AND uf.is_friend = FALSE
			""",
			[id])

			pending_request_count = curs.fetchone()[0]

	return render_template('/users/friends/index.html', friends = friends, pending_request_count = pending_request_count, pending_requests = pending_requests, friend_count = friend_count, current_user = id)

@user_friends_controller.route('/<int:id>/friends/', methods=['POST'])
def remove(id):
	if 'user_to_get' in request.form:
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

	elif 'cancel_request' in request.form:
		second_user_id = request.form['cancel_request']
		with psycopg2.connect(foodle.app.config['dsn']) as conn:
			with conn.cursor(cursor_factory=DictCursor) as curs:
				curs.execute(
				"""
				DELETE FROM user_friends
	        	WHERE user_id = %s
	        	AND friend_id = %s
	        	AND is_friend = False
	        	""",
	        	[id, second_user_id])

	return redirect("users/"+ str(id) + "/friends/", code=302)

@user_friends_controller.route('/<int:id>/friends/search', methods=['POST'])
def search(id):
	limit = request.args.get('limit') or 20
	offset = request.args.get('offset') or 0

	string_to_search = request.form['search_friend']
	with psycopg2.connect(foodle.app.config['dsn']) as conn:
		with conn.cursor(cursor_factory=DictCursor) as curs:
			curs.execute(
			"""
			SELECT u.id,count(u.id), u.username, u.display_name, ui.url, u.inserted_at
        	FROM user_friends AS uf
        	INNER JOIN users AS u ON u.id = uf.friend_id
        	INNER JOIN user_images AS ui ON ui.user_id = u.id
        	WHERE uf.user_id = %s
        	AND (u.display_name ILIKE %s OR u.username ILIKE %s ESCAPE '=')
        	AND uf.is_friend = TRUE
        	GROUP BY u.id, ui.url
        	LIMIT %s
        	OFFSET %s
        	""",
        	[id,'%' + string_to_search + '%', '%' + string_to_search + '%', limit, offset])
			friends = curs.fetchall()

			if friends:
				friend_count = friends[0][1];
			else:
				friend_count = 0;

			curs.execute(
			"""
			SELECT u.id,count(u.id) prc, u.username, u.display_name, ui.url, u.inserted_at
			FROM user_friends AS uf
			INNER JOIN users AS u ON u.id = uf.friend_id
			INNER JOIN user_images AS ui ON ui.user_id = u.id
			WHERE uf.user_id = %s
			AND (u.display_name ILIKE %s OR u.username ILIKE %s ESCAPE '=')
			AND uf.is_friend = FALSE
			GROUP BY u.id, ui.url
			""",
			[id,'%' + string_to_search + '%', '%' + string_to_search + '%'])

			pending_requests = curs.fetchall()

			if pending_requests:
				pending_request_count = pending_requests[0][1];
			else:
				pending_request_count = 0;


	return render_template('/users/friends/index.html', friends = friends,pending_request_count = pending_request_count, pending_requests = pending_requests, friend_count = friend_count, current_user = id)

@user_friends_controller.route('/<int:id>/friends/new_friend', methods=['GET'])
def new_friend(id):
        limit = request.args.get('limit') or 20
        offset = request.args.get('offset') or 0

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
                with conn.cursor(cursor_factory=DictCursor) as curs:
                        curs.execute(
                        """
                        SELECT u.id, u.username, u.display_name, u.inserted_at, ui.url
                        FROM users u, user_friends uf, user_images ui
                  		WHERE u.id = ui.user_id AND u.id != %s
                  		EXCEPT
                  		SELECT u.id, u.username, u.display_name, u.inserted_at, ui.url
        				FROM user_friends AS uf, users AS u 
        				INNER JOIN user_images AS ui ON ui.user_id = u.id
        				WHERE (uf.user_id = %s AND u.id = uf.friend_id)
        				OR  (uf.friend_id =%s AND u.id = uf.user_id)
                        LIMIT %s
                        OFFSET %s
                        """,
                        [id, id, id, limit, offset])

                        users = curs.fetchall()

        return render_template('/users/friends/new_friend.html', users = users, current_user = id)

@user_friends_controller.route('/<int:id>/friends/new_friend/<int:request_id>', methods=['GET'])
def send_friend_request(id,request_id):
	with psycopg2.connect(foodle.app.config['dsn']) as conn:
		with conn.cursor(cursor_factory=DictCursor) as curs:
			curs.execute(
			"""
			INSERT INTO user_friends
			(user_id, friend_id, is_friend)
			VALUES(%s, %s, False)
			""",
			[id, request_id])


	return redirect("users/"+ str(id) + "/friends/new_friend", code=302)