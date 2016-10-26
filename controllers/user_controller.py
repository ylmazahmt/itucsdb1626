from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/')
def index():
    return render_template('home.html', methods=['GET'])

@user_controller.route('/<int:id>')
def show(id):
    return render_template('search.html', methods=['GET'])

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
