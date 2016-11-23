#!/usr/bin/env python3
import foodle
import psycopg2
from flask import Blueprint, render_template, redirect

application_controller = Blueprint('application_controller', __name__)

@application_controller.route('/', methods=['GET'])
def index():
    return redirect('/users/2/feed')
