from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import User

application_controller = Blueprint('application_controller', __name__)

@application_controller.route('/', methods=['GET'])
def index():
    return render_template('/index.html')
