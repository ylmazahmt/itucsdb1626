#!/usr/bin/env python3
from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app
from models import User

session_controller = Blueprint('session_controller', __name__)

@session_controller.route('/new', methods=['GET'])
def new():
    return render_template('/sessions/new.html')

@session_controller.route('/', methods=['POST'])
def create():
    return None
