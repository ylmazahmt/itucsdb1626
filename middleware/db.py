import psycopg2 as db

connection = None

def __init__(dsn):
    global connection

    connection = db.connect(dsn)

    connection.cursor().execute(
    """
    SET search_path = \"$user\",main
    """)

    connection.commit()
