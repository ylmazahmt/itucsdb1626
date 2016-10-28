import psycopg2
from middleware import db
from models.error_handling import AbstractOperationException
from models import User

class Place:
    """
    The model class representing places.
    """

    def __init__(self, name, description, owner_id, persisted=False):
        """
        Initializes a new instance of place.
        """

        self.id = None
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self._persisted = persisted
        

    @staticmethod
    def All(limit=20, offset=0):
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT *
        FROM places
        LIMIT %s
        OFFSET %s
        """,
        [limit, offset])

        objects = cursor.fetchall()
        db.connection.commit()

        places = []

        for each_object in objects:
            place = Place(each_object[1], each_object[2], each_object[3], True)
            place.id = each_object[0]
            place.inserted_at = each_object[4]
            places.append(place)

        return places


    @staticmethod
    def One(id):
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT *
        FROM places
        WHERE id = %s
        LIMIT 1
        """,
        [id])

        data = cursor.fetchone()
        db.connection.commit()

        if data is not None:
            place = Place(data[1], data[2], data[3], True)
            place.id = data[0]
            place.inserted_at = data[4]

            return place
        else:
            return None


    @staticmethod
    def Count():
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT count(id)
        FROM places
        """)

        count = cursor.fetchone()[0]
        db.connection.commit()

        return count


    def save(self):
        """
        Persists the place in the database.
        """

        cursor = db.connection.cursor()

        if not self._persisted:
            cursor.execute(
            """
            INSERT INTO places
            (name, description, user_id)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            [self.name, self.description, self.owner_id])

            self.id = cursor.fetchone()[0]
        else:
            cursor.execute(
            """
            UPDATE places
            SET name = %s,
                description = %s,
                user_id = %s
            WHERE id = %s
            """,
            [self.name, self.description, self.owner_id, self.id])

        db.connection.commit()
        self._persisted = True


    def owner(self):
        """
        Fetches the user of the place.
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
