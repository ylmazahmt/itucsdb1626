#!/usr/bin/env python3
from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import User

feed_controller = Blueprint('feed_controller', __name__)

@feed_controller.route('/<int:id>/feed/', methods=['GET'])
def index(id):
    return render_template('/users/feed/index.html')
