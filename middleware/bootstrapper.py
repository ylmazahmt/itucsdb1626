from middleware import db
import bcrypt

def __init__():
    connection = db.connection

    cursor = connection.cursor()

    cursor.execute(open("sql/init.sql", "r").read())

    cursor.execute("INSERT INTO users (username, password_digest, email) VALUES (%s, %s, %s) RETURNING id", ["admin", bcrypt.hashpw("test".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "test@mail.com"])

    cursor.execute("INSERT INTO user_activations (user_id) VALUES (%s)", [cursor.fetchone()[0]])

    cursor.execute("INSERT INTO users (username, password_digest, email) VALUES (%s, %s, %s) RETURNING id", ["gugar", bcrypt.hashpw("test".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "gugar@mail.com"])

    cursor.execute("INSERT INTO user_friends (user_id, friend_id, is_friend) VALUES (1,2,False)")

    connection.commit()
