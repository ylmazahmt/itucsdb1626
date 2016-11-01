#!/usr/bin/env python3
import foodle
import psycopg2
from flask import Blueprint, render_template
from flask import current_app

application_controller = Blueprint('application_controller', __name__)

@application_controller.route('/', methods=['GET'])
def index():
    return render_template('/index.html')
