import psycopg2 as db

def init(dsn):
    with db.connect(dsn) as connection:
        cursor = connection.cursor()

        cursor.execute("DROP SCHEMA main CASCADE")
        cursor.execute("CREATE SCHEMA main")

        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

        cursor.execute("""CREATE TABLE users(
                            id SERIAL PRIMARY KEY,
                            username character varying(255) UNIQUE NOT NULL,
                            password character varying(255) NOT NULL,
                            email character varying(255) UNIQUE NOT NULL,
                            activation_key uuid DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
                            inserted_at timestamp DEFAULT now() NOT NULL
                      )""")

        cursor.execute("""CREATE TABLE user_activations(
                            user_id integer PRIMARY KEY,
                            inserted_at timestamp DEFAULT now() NOT NULL,
                            FOREIGN KEY ("user_id") REFERENCES users(id)
                      )""")

    connection.commit()
