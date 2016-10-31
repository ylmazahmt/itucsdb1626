from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import CheckIn
check_ins_controller = Blueprint('check_ins_controller', __name__)

@check_ins_controller.route('/', methods=['GET'])
def index():
    checkins = CheckIn.All()

    return render_template('/checkins/index.html', checkins=checkins)

@check_ins_controller.route('/<int:id>', methods=['GET'])
def show(id):
    checkin = CheckIn.One(id)

    return render_template('/checkins/show.html', checkin=checkin)

@check_ins_controller.route('/', methods=['POST'])
def create():
    return None

@check_ins_controller.route('/new', methods=['GET'])
def new():
    return render_template('/checkins/new.html')

@check_ins_controller.route('/<int:id>', methods=['DELETE'])
def delete():
  return None
