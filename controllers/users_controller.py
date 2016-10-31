from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import User

users_controller = Blueprint('users_controller', __name__)

@users_controller.route('/', methods=['GET'])
def index():
    users = User.All()

    return render_template('/users/index.html', users=users)

@users_controller.route('/<int:id>', methods=['GET'])
def show(id):
    user = User.One(id)

    if user is not None:

        return render_template('users/show.html', user=user)
    else:

        return "Entity not found.", 404

@users_controller.route('/', methods=['POST'])
def create():
    return None

@users_controller.route('/new', methods=['GET'])
def new():
    return render_template('/users/new.html')

@users_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    return None

@users_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    return None

@users_controller.route('/<int:id>', methods=['DELETE'])
def delete():
    return None
