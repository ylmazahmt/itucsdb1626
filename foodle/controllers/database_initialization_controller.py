from flask import Blueprint

database_initialization_controller = Blueprint('database_initialization_controller', __name__)

@database_initialization_controller.route('/', methods=['POST'])
def create():
    from middleware import bootstrapper

    bootstrapper.__init__()

    return "Successfully initialized persistence layer.", 201
