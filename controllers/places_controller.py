from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import Place

places_controller = Blueprint('places_controller', __name__)

@places_controller.route('/', methods=['GET'])
def index():
    places = Place.All()
    count = Place.Count()

    return render_template('/places/index.html', places=places, count=count)

@places_controller.route('/<int:id>', methods=['GET'])
def show(id):
    place = Place.One(id)

    return render_template('/places/show.html', place=place)

@places_controller.route('/', methods=['POST'])
def create():
    return None

@places_controller.route('/new', methods=['GET'])
def new():
    return render_template('/places/new.html')

@places_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    return None

@places_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    return None

@places_controller.route('/<int:id>', methods=['DELETE'])
def delete():
    return None
