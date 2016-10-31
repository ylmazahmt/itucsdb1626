from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import CheckIn
check_ins_controller = Blueprint('check_ins_controller', __name__)


@check_ins_controller.route('/', methods=['GET'])
def index():
    check_ins = CheckIn.All()

    return render_template('/check_ins/index.html', check_ins=check_ins)


@check_ins_controller.route('/<int:id>', methods=['GET'])
def show(id):
    check_in = CheckIn.One(id)

    if check_in is not None:

        return render_template('/check_ins/show.html', check_in=check_in)
    else:

        return "Entity not found.", 404


@check_ins_controller.route('/', methods=['POST'])
def create():
    return None


@check_ins_controller.route('/new', methods=['GET'])
def new():
    return render_template('/check_ins/new.html')


@check_ins_controller.route('/<int:id>', methods=['DELETE'])
def delete(id):
    check_in = CheckIn.One(id)

    if check_in is not None:
        check_in.delete()

        return "", 204
    else:

        return "Entity not found.", 404
