from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import User

user_image_controller = Blueprint('user_image_controller', __name__)

@user_controller.route('/<int:id>/image', methods=['GET'])
def show(id):
    return render_template('search.html')

@user_controller.route('/<int:id>', methods=['POST'])
def create():
    return None

@user_controller.route('/<int:id>/image', methods=['PUT', 'PATCH'])
def update(id):
    return None

@user_controller.route('/<int:id>/image', methods=['DELETE'])
def delete():
    return None
