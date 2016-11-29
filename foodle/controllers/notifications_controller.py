#!/usr/bin/env python3
import foodle
import psycopg2
from psycopg2.extras import DictCursor
from flask import Blueprint, render_template, current_app, request, redirect

notifications_controller = Blueprint('notifications_controller', __name__)

@notifications_controller.route('/', methods=['GET'])
def index():
    return None
