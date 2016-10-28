import psycopg2
from middleware import db
from models.error_handling import AbstractOperationException
from models import User

class Post:
    """
    The model class representing posts, who belong to places.
    """

    def __init__(self, body, owner_id, persisted=False):
        """
        Initializes a new instance of post.
        """

        self.id = None
        self.body = body
        self.owner_id = owner_id
        self._persisted = persisted

    @staticmethod
    def All(limit=20, offset=0):
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT *
        FROM posts
        LIMIT %s
        OFFSET %s
        """,
        [limit, offset])

        objects = cursor.fetchall()
        db.connection.commit()
        posts = []

        for each_object in objects:
            post = Post(each_object[1], each_object[2], True)
            post.id = each_object[0]
            post.inserted_at = each_object[3]
            posts.append(post)

        return posts


    @staticmethod
    def One(id):
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT *
        FROM posts
        WHERE id = %s
        LIMIT 1
        """,
        [id])

        data = cursor.fetchone()
        db.connection.commit()

        if data is not None:
            post = Post(data[1], data[2], True)
            post.id = data[0]
            post.inserted_at = data[3]

            return post
        else:
            return None


    @staticmethod
    def Count():
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT count(id)
        FROM posts
        """)

        count = cursor.fetchone()[0]
        db.connection.commit()

        return count


    def save(self):
        """
        Persists the post in the database.
        """

        cursor = db.connection.cursor()

        if not self._persisted:
            cursor.execute(
            """
            INSERT INTO posts
            (body, user_id)
            VALUES (%s, %s)
            RETURNING id
            """,
            [self.body, self.owner_id])

            self.id = cursor.fetchone()[0]
        else:
            cursor.execute(
            """
            UPDATE posts
            SET body = %s,
                user_id = %s
            WHERE id = %s
            """,
            [self.body, self.owner_id])

        db.connection.commit()
        self._persisted = True

    def owner(self):
        """
        Fetches the user of the post.
        """

        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT id, username, email, inserted_at
        FROM users
        WHERE id = %s
        """,
        [self.owner_id])

        data = cursor.fetchone()

        db.connection.commit()

        user = User(data[1], None, data[2], True)
        user.id = data[0]
        user.inserted_at = data[3]

        return user
