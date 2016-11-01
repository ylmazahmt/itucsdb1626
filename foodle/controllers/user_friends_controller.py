#!/usr/bin/env python3
from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app
from flask import request

from models import User

user_friends_controller = Blueprint('user_friends_controller', __name__)

@user_friends_controller.route('/<int:id>/friends/', methods=['GET','POST'])
def index(id):
	user = User.One(id)
	if request.method == 'GET':
		friends = user.friends()

	elif 'search_friend' in request.form:
		str_s = request.form['search_friend']
		friends = user.find_in_friends(str_s)

	requests = user.pending_requests()
	friend_count = user.count_friends()
	request_count = user.count_requests()

	return render_template('/users/friends/index.html', friends = friends, requests = requests, friend_count = friend_count, request_count = request_count)

@user_friends_controller.route('/<int:id>/addasfriend', methods=['POST'])
def addasfriend(session_owner, id):
    return None

@user_friends_controller.route('/<int:id>/deletefriend', methods=['POST'])
def deletefriend(session_owner, id):
    return None
