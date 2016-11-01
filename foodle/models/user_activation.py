from middleware import db

class UserActivation:
    """
    Represents a user activation entity, which belongs to a user.
    """

    def __init__(self, user_id, persisted=False):
        self.user_id = user_id
        self._persisted = persisted


    @staticmethod
    def All(limit=20, offset=0):
        """
        Returns all of the user activations.
        """

        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT *
        FROM user_activations
        LIMIT %s
        OFFSET %s
        """,
        [limit, offset])

        objects = cursor.fetchall()
        user_activations = []

        for each_object in objects:
            user_activation = User(each_object[1], True)
            user_activation.id = each_object[0]
            user_activation.inserted_at = each_object[2]
            user_activations.append(user_activation)

        return user_activations


    @staticmethod
    def One(id):
        """
        Returns the user activation with given identifier.
        """

        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT *
        FROM user_activations
        WHERE id = %s
        LIMIT 1
        """,
        [id])

        data = cursor.fetchone()

        if data is not None:
            user_activation = User(data[1], True)
            user_activation.id = data[0]
            user_activation.inserted_at = data[2]

            return user_activation
        else:
            return None


    def save(self):
        """
        Persists the user activation in the database.
        """

        cursor = db.connection.cursor()

        if not self._persisted:
            cursor.execute(
            """
            INSERT INTO user_activations
            (user_id)
            VALUES (%s)
            RETURNING id
            """,
            [self.user_id])

            self.id = cursor.fetchone()[0]
        else:
            cursor.execute(
            """
            UPDATE user_activations
            SET user_id = %s
            WHERE id = %s
            """,
            [self.user_id, self.id])

        db.connection.commit()
        self._persisted = True
