#!/usr/bin/env python3
import os
import foodle
import psycopg2
from foodle import app
from foodle.db import init
from foodle.router import bootstrap
from flask_login import LoginManager
from psycopg2.extras import DictCursor

login_manager = LoginManager()

@login_manager.user_loader
def deserialize_user(id):
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
            """
            SELECT u.id, u.username, u.display_name, u.inserted_at
            FROM users u
            WHERE u.id = %s
            """,
            [id])

            obj = curs.fetchone()

            if obj is not None:
                return User(True, obj['id'], obj['username'], obj['inserted_at'], obj['display_name'])

if __name__ == "__main__":
    app_port = os.getenv('VCAP_APP_PORT')

    if app_port is not None:
        port, debug = int(app_port), False
    else:
        port, debug = 5000, True

    init()
    bootstrap()

    login_manager.init_app(app)

    app.config['WTF_CSRF_ENABLED'] = False
    app.secret_key = os.urandom(24)

    app.run(host='0.0.0.0', port=port, debug=debug)
