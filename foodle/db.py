#!/usr/bin/env python3
import foodle
import bcrypt
import psycopg2
import os

def init():
    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor() as curs:
            curs.execute(open("foodle/sql/init.sql", "r").read())

            curs.execute("INSERT INTO users (username, password_digest, ip_address) VALUES (%s, %s, %s) RETURNING id", ["admin", bcrypt.hashpw("test".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "0.0.0.0"])

            id = curs.fetchone()[0]

            curs.execute("INSERT INTO user_activations (user_id) VALUES (%s)", [id])
            curs.execute("INSERT INTO user_emails (user_id, email) VALUES (%s, %s)", [id, "admin@mail.com"])

            if os.environ.get('NO_SEED') is None:
                curs.execute(open("foodle/sql/seed.sql", "r").read())

            conn.commit()
