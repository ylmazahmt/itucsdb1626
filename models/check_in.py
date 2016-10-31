import psycopg2
from middleware import db
from models.error_handling import AbstractOperationException
from models import User
from models import Place

class CheckIn:
    """
    The model class representing checkins.
    """

    def __init__(self, owner_id, place_id, persisted=False):
        """
        Initializes a new instance of checkin.
        """

        self.id = None
        self.owner_id = owner_id
        self.place_id = place_id
        self._persisted = persisted

    @staticmethod
    def All(limit=20, offset=0):
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT *
        FROM checkins
        LIMIT %s
        OFFSET %s
        """,
        [limit, offset])

        data = cursorfetchall()
        db.connection.commit()
        checkins = []

        for each_data in data:
            checkin = CheckIn(each_data[1], each_data[2], True)
            checkin.id = each_data[0]
            checkin.inserted_at = each_data[3]
            checkins.append(checkin)

        return checkins


    @staticmethod
    def One(id):
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT *
        FROM checkins AS c
        WHERE c.id = %s
        LIMIT 1
        """,
        [id])

        data = cursor.fetchone()
        db.connection.commit()

        checkin = CheckIn(data[1], data[2], True)
        checkin.id = data[0]
        checkin.inserted_at = data[3]

        return checkin


    @staticmethod
    def Count():
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT count(id)
        FROM checkins
        """)

        count = cursor.fetchone()[0]
        db.connection.commit()

        return count


    def save(self):
        """
        Persists the checkin in the database.
        """

        cursor = db.connection.cursor()

        if not self._persisted:
            cursor.execute(
            """
            INSERT INTO checkins
            (user_id, place_id)
            VALUES (%s, %s)
            RETURNING id, inserted_at
            """,
            [self.owner_id, self.place_id])

            data = cursor.fetchone()

            self.id = data[0]
            self.inserted_at = data[1]
        else:
            cursor.execute(
            """
            UPDATE checkins
            SET user_id = %s,
                place_id = %s
            WHERE id = %s
            """,
            [self.owner_id, self.place_id, self.id])

        db.connection.commit()
        self._persisted = True


    def owner(self):
        """
        Returns the owner user of the checkin.
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


    def place(self):
        """
        Returns the place of the checkin.
        """

        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT *
        FROM places
        WHERE id = %s
        """,
        [self.place_id])

        data = cursor.fetchone()

        db.connection.commit()

        place = Place(data[1], data[2], data[3], True)
        place.id = data[0]
        place.inserted_at = data[4]

        return place
