from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import User

import psycopg2
from middleware import db

def id_to_user(user_id):

	#create a user object of given id
	cursor = db.connection.cursor()

	cursor.execute(
	"""
	SELECT id, username, email, inserted_at
	FROM users
	WHERE id = %s
	LIMIT 1
	""",
	[user_id])

	data = cursor.fetchall()

	if data is not None:
		user = User(data[0][1], None, data[0][2], True)
		user.id = data[0][0]
		user.inserted_at = data[0][3]

		return user
	else:
		return None
	
def all_friends(user, limit=20, offset=0):

	#fetch all friends of given user
	cursor = db.connection.cursor()

	cursor.execute(
	"""
	SELECT friend_id
	FROM user_friends
	WHERE user_id = %s
	AND is_friend
	LIMIT %s
	OFFSET %s
	""",
	[user.id, limit, offset])

	objects = cursor.fetchall()

	friends = []

	for each_object in objects:
		friend = id_to_user(each_object)
		friends.append(friend)

	return friends

def count_friends(user):

	#count friends of given user
	cursor = db.connection.cursor()

	cursor.execute(
	"""
	SELECT count(id)
	FROM user_friends
	WHERE user_id = %s
	AND is_friend
	""",
	[user.id])

	count = cursor.fetchone()[0]
	db.connection.commit()

	return count

def pending_requests(user, limit=20, offset=0):

	#fetch all pending requests of given user
	cursor = db.connection.cursor()

	cursor.execute(
	"""
	SELECT user_id
	FROM user_friends
	WHERE friend_id = %s
	AND is_friend = False
	LIMIT %s
	OFFSET %s
	""",
	[user.id, limit, offset])

	objects = cursor.fetchall()

	requests = []

	for each_object in objects:
		request = id_to_user(each_object)
		requests.append(request)

	return requests

def count_requests(user):

	#count pending requests of given user
	cursor = db.connection.cursor()

	cursor.execute(
	"""
	SELECT count(id)
	FROM user_friends
	WHERE friend_id = %s
	AND is_friend = False
	""",
	[user.id])

	count = cursor.fetchone()[0]
	db.connection.commit()

	return count

def is_friend_or_pending(first_user, second_user):

	# value = 3, friend request sent
	# value = 2, friend
	# value = 1, pending request
	# value = 0, total stranger

	cursor = db.connection.cursor()

	cursor.execute(
	"""
	SELECT user_id
	FROM user_friends 
	WHERE (user_id = %s
	AND friend_id = %s)
	OR (user_id = %s
	AND friend_id = %s);
	""",
	[first_user.id, second_user.id, second_user.id, first_user.id])

	data = cursor.fetchall() 

	if len(data) == 1:
		if data[0][0] == first_user.id:
			return 3
		else:
			return 1
	else:
		return len(data) # 0 or 2

def add_friend(first_user, second_user):
	"""
	add or update relevant relationship information about two given users
	"""
	relationship = is_friend_or_pending(first_user, second_user)

	if relationship == 2 or relationship == 3:
		return False

	cursor = db.connection.cursor()

	#send friend request
	if relationship == 0:
		cursor.execute(
		"""
		INSERT INTO user_friends
		(user_id, friend_id, is_friend)
		VALUES(%s, %s, False)
		""",
		[first_user.id, second_user.id])


	#accept the friend request
	elif relationship == 1:
		cursor.execute(
		"""
		INSERT INTO user_friends
		(user_id, friend_id, is_friend)
		VALUES(%s, %s, True)
		""",
		[first_user.id, second_user.id])

		cursor.execute(
		"""
		UPDATE user_friends
		SET is_friend = True
		WHERE user_id = %s
		AND friend_id = %s
		""",
		[second_user.id, first_user.id])
	
	db.connection.commit()

	return True


user_friends_controller = Blueprint('user_friends_controller', __name__)

@user_friends_controller.route('/<int:id>/friends/', methods=['GET'])
def index(id):
	friends = all_friends(id_to_user(id))
	requests = pending_requests(id_to_user(id))
	friend_count = count_friends(id_to_user(id))
	request_count = count_requests(id_to_user(id))

	return render_template('/users/friends/index.html', friends = friends, requests = requests, friend_count = friend_count, request_count = request_count)

@user_friends_controller.route('/<int:id>/addasfriend', methods=['POST'])
def addasfriend(session_owner, id):
    return None

@user_friends_controller.route('/<int:id>/deletefriend', methods=['POST'])
def deletefriend(session_owner, id):
    return None