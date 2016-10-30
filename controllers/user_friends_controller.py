from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app
from flask import request

from models import User

user_friends_controller = Blueprint('user_friends_controller', __name__)

@user_friends_controller.route('/<int:id>/friends/', methods=['GET','POST'])
def index(id):
	if request.method == 'GET':
		friends = User.all_friends(User.get_user(id))

	elif 'search_friend' in request.form:
		str_s = request.form['search_friend']
		friends = User.find_in_friends(User.get_user(id),str_s)

	requests = User.pending_requests(User.get_user(id))
	friend_count = User.count_friends(User.get_user(id))
	request_count = User.count_requests(User.get_user(id))

	return render_template('/users/friends/index.html', friends = friends, requests = requests, friend_count = friend_count, request_count = request_count)

@user_friends_controller.route('/<int:id>/addasfriend', methods=['POST'])
def addasfriend(session_owner, id):
    return None

@user_friends_controller.route('/<int:id>/deletefriend', methods=['POST'])
def deletefriend(session_owner, id):
    return None
