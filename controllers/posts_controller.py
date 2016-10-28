from flask import Blueprint, render_template
from datetime import datetime
from flask import current_app

from models import Post

posts_controller = Blueprint('posts_controller', __name__)

@posts_controller.route('/', methods=['GET'])
def index():
    posts = Post.All()
    count = Post.Count()

    return render_template('/posts/index.html', posts=posts, count=count)

@posts_controller.route('/<int:id>', methods=['GET'])
def show(id):
    post = Post.One(id)

    return render_template('/posts/show.html', place=place)

@posts_controller.route('/', methods=['POST'])
def create():
    return None

@posts_controller.route('/new', methods=['GET'])
def new():
    return render_template('/posts/new.html')

@posts_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    return None

@posts_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    return None

@posts_controller.route('/<int:id>', methods=['DELETE'])
def delete():
    return None
