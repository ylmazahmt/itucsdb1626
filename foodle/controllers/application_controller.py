#!/usr/bin/env python3
import foodle
import psycopg2
import jwt
from flask import Blueprint, render_template, redirect, request, current_app

application_controller = Blueprint('application_controller', __name__)

@application_controller.route('/', methods=['GET'])
def index():
    token = request.cookies.get('jwt')

    if token is not None:
        try:
            current_user = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])

            return redirect('/users/' + str(current_user['id']) + '/feed')
        except:
            return redirect('/sessions/new')

    return redirect('/sessions/new')
