from middleware import db
import bcrypt

def __init__():
    connection = db.connection

    cursor = connection.cursor()

    cursor.execute("DROP SCHEMA main CASCADE")
    cursor.execute("CREATE SCHEMA main")

    cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

    cursor.execute(
    """
    CREATE TABLE users(
        id SERIAL PRIMARY KEY,
        username character varying(255) UNIQUE NOT NULL,
        password_digest character varying(255) NOT NULL,
        email character varying(255) UNIQUE NOT NULL,
        activation_key uuid DEFAULT "public".uuid_generate_v4() UNIQUE NOT NULL,
        inserted_at timestamp DEFAULT now() NOT NULL
    )
    """)

    cursor.execute(
    """
    CREATE TABLE user_activations(
        user_id integer PRIMARY KEY,
        inserted_at timestamp DEFAULT now() NOT NULL,
        FOREIGN KEY ("user_id") REFERENCES users(id)
    )
    """)

    cursor.execute("INSERT INTO users (username, password_digest, email) VALUES (%s, %s, %s) RETURNING id", ["admin", bcrypt.hashpw("test".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "test@mail.com"])

    cursor.execute("INSERT INTO user_activations (user_id) VALUES (%s)", [cursor.fetchone()[0]])

    cursor.execute(
    """
    CREATE TABLE user_images(
        user_id integer PRIMARY KEY,
        data bytea NOT NULL,
        inserted_at timestamp DEFAULT now() NOT NULL,
        FOREIGN KEY ("user_id") REFERENCES users(id)
    )
    """)

    connection.commit()
