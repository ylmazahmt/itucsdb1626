from flask import Blueprint, render_template

from datetime import datetime
from flask import current_app

www = Blueprint('www', __name__)

@www.route('/')
def home_page():
    return render_template('home.html')

@www.route('/search')
def search():
    return render_template('search.html')

@www.route('/cities')
def cities():
    return render_template('cities.html')

@www.route('/friends')
def friends():
    return render_template('friends.html')

@www.route('/places')
def places():
    return render_template('places.html')
