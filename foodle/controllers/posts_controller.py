import foodle
import psycopg2
from flask import Blueprint, render_template, current_app, request, redirect

posts_controller = Blueprint('posts_controller', __name__)

@posts_controller.route('/', methods=['GET'])
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 20

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM posts
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            posts = curs.fetchall()

            curs.execute(
            """
            SELECT count(id)
            FROM posts
            """)

            count = curs.fetchone()[0]

            return render_template('/posts/index.html', posts=posts, count=posts)

@posts_controller.route('/<int:id>', methods=['GET'])
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM posts
            WHERE id = %s
            """,
            [id])

            post = curs.fetchone()

            if post is not None:
                return render_template('/posts/show.html', post=post)
            else:
                return "Entity not found.", 404


@posts_controller.route('/', methods=['POST'])
def create():
    if not isinstance(request.json.get('body'), str) or not isinstance(request.json.get('user_id'), int):
        return "Request body is unprocessable.", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO posts
            (body, user_id)
            VALUES (%(body)s, %(user_id)s)
            RETURNING *
            """, request.json)

            if curs.rowcount is not 0:
                return render_template('/posts/show.html', post=curs.fetchone())
            else:
                return "Entity not found.", 404


@posts_controller.route('/new', methods=['GET'])
def new():
    return render_template('/posts/new.html')

@posts_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    if request.json.get('id') is not None or not isinstance(request.json.get('name'), str) or not isinstance(request.json.get('user_id'), int):
        return "Request body is unprocessable.", 422

    request.json['id'] = id

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE posts
            SET body = %(body)s,
                user_id = %(user_id)s
            WHERE id = %(id)s
            RETURNING *
            """, request.json)

            if curs.rowcount is not 0:
                return render_template('/posts/show.html', post=curs.fetchone())
            else:
                return "Entity not found.", 404


@posts_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    return None

@posts_controller.route('/<int:id>', methods=['DELETE'])
def delete():
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM posts
            WHERE id = %s
            """, [id])

            if curs.rowcount is not 0:
                return redirect('/posts/index.html')
            else:
                return "Entity not found.", 404
