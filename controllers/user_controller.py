from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import User

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/', methods=['GET'])
def index():
    users = User.All()

    return render_template('/users/index.html', users=users)

@user_controller.route('/<int:id>', methods=['GET'])
def show(id):
    return render_template('search.html')

@user_controller.route('/', methods=['POST'])
def create():
    return None

@user_controller.route('/new', methods=['GET'])
def new():
    return render_template('/users/new.html')

@user_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    return None

@user_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    return None

@user_controller.route('/<int:id>', methods=['DELETE'])
def delete():
    return None
