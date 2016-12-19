import foodle
import psycopg2
from psycopg2.extras import DictCursor
from foodle.utils.auth_hook import auth_hook_functor
from flask import Blueprint, render_template, current_app, request, make_response, g

chat_room_messages_controller = Blueprint('chat_room_messages_controller', __name__)

@chat_room_messages_controller.route('/',methods=['GET'])
@auth_hook_functor
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 0

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT crm.id, cr.name, crm.body, u.username
            FROM chat_room_messages as crm
            INNER JOIN users as u ON crm.user_id=u.id
            INNER JOIN chat_rooms as cr ON crm.chat_room_id = cr.id
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            chat_room_messages=curs.fetchall()

            curs.execute(
            """
            SELECT count(id)
            FROM chat_room_messages
            """)
            count = curs.fetchone()[0]

            return render_template('/chat_room_messages/index.html',chat_room_messages=chat_room_messages,count=count)

@chat_room_messages_controller.route('/<int:id>', methods=['GET'])
@auth_hook_functor
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM chat_room_messages AS crm
            INNER JOIN users AS u ON u.id=crm.user_id
            WHERE crm.id = %s
            """,
            [id])

            chat_room_message=curs.fetchone()
            if chat_room_message is not None:
                return render_template('chat_room_messages/show.html', chat_room_message=chat_room_message)
            else:
                return "Chat Room Message not found.", 404

@chat_room_messages_controller.route('/', methods=['POST'])
@auth_hook_functor
def create():
    user_id = int(request.json.get('user_id'))
    chat_room_id = int(request.json.get('chat_room_id'))
    body = request.json.get('body')

    if not isinstance(user_id, int) or not isinstance(body, str) or not isinstance(chat_room_id, int):
        return "Request rating is unprocessable", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO chat_room_messages
            (user_id, chat_room_id, body)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            [user_id, chat_room_id, body])

            chat_room_message=curs.fetchone()
            resp = make_response()
            resp.headers['location'] = '/chat_room_messages/' + str(chat_room_message['id'])

            return resp, 201

@chat_room_messages_controller.route('/new', methods=['GET'])
@auth_hook_functor
def new():
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT id, username
            FROM users
            """,
            )

            users = curs.fetchall()

            curs.execute(
            """
            SELECT id, name
            FROM chat_rooms
            """,
            )

            chat_rooms = curs.fetchall()


    return render_template('/chat_room_messages/new.html',users=users,chat_rooms=chat_rooms)

@chat_room_messages_controller.route('/<int:id>', methods=['PUT','PATCH'])
@auth_hook_functor
def update(id):
    body = request.json['body']
    if request.json.get('id') is not None or not isinstance(body,str):
        return "Request is unprocessable", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE chat_room_messages
            SET body = %s
            WHERE id = %s
            """,
            [body,id])

            if curs.rowcount is not 0:
                resp = make_response()
                resp.headers['location'] = '/chat_room_messages/' + str(id)
                return resp, 200
            else:
                return "Chat Room Message not found.", 404


@chat_room_messages_controller.route('/<int:id>/edit', methods=['GET'])
@auth_hook_functor
def edit(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM chat_room_messages
            WHERE id = %s
            """,
            [id])

            chat_room_message = curs.fetchone()

            if chat_room_message is not None:
                return render_template('/chat_room_messages/edit.html',chat_room_message=chat_room_message)
            else:
                return "Chat Room Message not found.", 404

@chat_room_messages_controller.route('/<int:id>',methods=['DELETE'])
@auth_hook_functor
def delete(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM chat_room_messages
            WHERE id = %s
            """,
            [id])
            if curs.rowcount is not 0:
                return "", 204
            else:
                return "Chat Room Message not found.", 404
