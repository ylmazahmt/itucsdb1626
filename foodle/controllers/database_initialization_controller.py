from flask import Blueprint
from foodle.db import init

database_initialization_controller = Blueprint('database_initialization_controller', __name__)

@database_initialization_controller.route('/', methods=['POST'])
def create():
    # Instantiate the database adapter
    init()

    return "Successfully initialized persistence layer.", 203
