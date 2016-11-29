import foodle
import psycopg2
from psycopg2.extras import DictCursor, RealDictCursor

from flask import Blueprint, render_template, current_app, request, make_response

chat_rooms_controller = Blueprint('chat_rooms_controller', __name__)

@chat_rooms_controller.route('/',methods=['GET'])
def index():
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 0

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
            """
            SELECT cr.id, cr.name, u.username
            FROM chat_rooms as cr
            INNER JOIN users as u ON cr.user_id=u.id
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

            chat_rooms=curs.fetchall()

            curs.execute(
            """
            SELECT count(id)
            FROM chat_rooms
            """)
            count = curs.fetchone()['count']


            for chat_room in chat_rooms:
                curs.execute(
                """
                SELECT *
                FROM chat_room_messages
                WHERE chat_room_id = %s
                LIMIT 10
                """,
                [chat_room['id']])

                chat_room['chat_room_messages'] = curs.fetchall()


            return render_template('/chat_rooms/index.html',chat_rooms=chat_rooms,count=count)

@chat_rooms_controller.route('/<int:id>', methods=['GET'])
def show(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM chat_rooms
            WHERE id = %s
            """,
            [id])

            chat_room=curs.fetchone()

            curs.execute(
            """
            SELECT crm.id, cr.name, crm.body, u.username
            FROM chat_room_messages as crm
            INNER JOIN users as u ON crm.user_id=u.id
            INNER JOIN chat_rooms as cr ON crm.chat_room_id = cr.id
            WHERE crm.chat_room_id=%s
            """,
            [id])

            chat_room_messages=curs.fetchall()

            if chat_room is not None:
                return render_template('chat_rooms/show.html', chat_room=chat_room,chat_room_messages=chat_room_messages)
            else:
                return "Chat Room not found.", 404


@chat_rooms_controller.route('/', methods=['POST'])
def create():
    user_id = int(request.json['user_id'])
    name =  request.json['name']

    if not isinstance(user_id,int) or not isinstance(name,str):
        return "Request rating is unprocessable",422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            INSERT INTO chat_rooms
            (user_id, name)
            VALUES (%s, %s)
            RETURNING id
            """,
            [user_id, name])

            chat_room=curs.fetchone()
            resp = make_response()
            resp.headers['location'] = '/chat_rooms/' + str(chat_room['id'])

            return resp, 201

@chat_rooms_controller.route('/new', methods=['GET'])
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

    return render_template('/chat_rooms/new.html',users=users)

@chat_rooms_controller.route('/<int:id>', methods=['PUT','PATCH'])
def update(id):
    name = request.json['name']
    if request.json.get('id') is not None or not isinstance(name,str):
        return "Request is unprocessable", 422

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            UPDATE chat_rooms
            SET name = %s
            WHERE id = %s
            """,
            [name,id])

            if curs.rowcount is not 0:
                resp = make_response()
                resp.headers['location'] = '/chat_rooms/' + str(id)
                return resp, 200
            else:
                return "Chat Room not found.", 404

@chat_rooms_controller.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM chat_rooms
            WHERE id = %s
            """,
            [id])

            chat_room = curs.fetchone()

            if chat_room is not None:
                return render_template('/chat_rooms/edit.html',chat_room=chat_room)
            else:
                return "Chat Room not found.", 404

@chat_rooms_controller.route('/<int:id>',methods=['DELETE'])
def delete(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            DELETE FROM chat_rooms
            WHERE id = %s
            """,
            [id])
            if curs.rowcount is not 0:
                return "", 204
            else:
                return "Chat Room not found.", 404
