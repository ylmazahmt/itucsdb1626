from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import User

user_friends_controller = Blueprint('user_friends_controller', __name__)

@user_friends_controller.route('/<int:id>/friends/', methods=['GET'])
def index(id):
    return render_template('/users/friends/index.html')
