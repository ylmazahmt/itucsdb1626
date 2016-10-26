import bcrypt
import psycopg2
from middleware import db
from models.error_handling import AbstractOperationException

class User:
    """
    The user model class representing users of the application.
    """

    def __init__(self, username, password_digest, email, persisted=False):
        """
        Initializes a new instance of user.
        """

        self.id = None
        self.username = username
        self.password_digest = password_digest
        self.email = email
        self._persisted = persisted

    @staticmethod
    def All(limit=20, offset=0):
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT id, username, email, inserted_at
        FROM users
        LIMIT %s
        OFFSET %s
        """,
        [limit, offset])

        objects = cursor.fetchall()
        users = []

        for each_object in objects:
            user = User(each_object[1], None, each_object[2], True)
            user.id = each_object[0]
            user.inserted_at = each_object[3]
            users.append(user)

        return users

    def save(self):
        """
        Persists the user in the database.
        """

        cursor = db.connection.cursor()

        if self._persisted:
            cursor.execute(
            """
            INSERT INTO users
            (username, password_digest, email)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            [self.username, self.password_digest, self.email])

            self.id = cursor.fetchone()[0]
        else:
            cursor.execute(
            """
            UPDATE users
            SET username = %s,
                password_digest = %s,
                email = %s
            WHERE id = %s
            """,
            [self.username, self.password_digest, self.email, self.id])

        db.connection.commit()
        self._persisted = True


    def activate(self):
        """
        Persists the user activation object in the database.
        """

        if (self.id is not None) and (self._persisted is True):
            cursor = db.connection.cursor()

            try:
                cursor.execute(
                """
                INSERT INTO user_activations
                (user_id)
                VALUES (%s)
                """,
                [self.id])
            except psycopg2.IntegrityError as error:
                assert error.pgcode == "23505"
                assert error.diag.constraint_name == "user_activations_pkey"
                raise UserAlreadyActivatedException(self.id)
            except:
                raise

            db.connection.commit()
        else:
            raise AbstractOperationException("User::activate()", "user is not persisted")


    def is_active(self):
        """
        Returns the activation status of the user.
        """

        if (self.id is not None) and (self._persisted is True):
            cursor = db.connection.cursor()

            cursor.execute(
            """
            SELECT exists(
                SELECT *
                FROM user_activations
                WHERE user_id = %s
            )
            """,
            [self.id])

            return cursor.fetchone()[0] == True
        else:
            raise AbstractOperationException("User::is_active()", "user is not persisted")

    def get_image(self):
        """
        Returns the image of the user.
        """
        if (self.id is not None) and (self._persisted is True):
            cursor = db.connection.cursor()

            cursor.execute(
            """
            SELECT data
            FROM user_images
            WHERE user_id = %s
            """,
            [self.id])

            return cursor.fetchone()[0]
        else:
            raise AbstractOperationException("User::get_image()", "user is not persisted")

    def assign_image(self, image):
        """
        Assigns an image to the user.
        """

        # FIXME: Transaction support
        if (self.id is not None) and (self._persisted is True):
            cursor = db.connection.cursor()

            cursor.execute(
            """
            SELECT exists(
                SELECT data
                FROM user_images
                WHERE user_id = %s
            )
            """,
            [self.id])

            if cursor.fetchone()[0]:
                cursor.execute(
                """
                UPDATE user_images
                SET data = %s
                WHERE user_id = %s
                """,
                [image, self.id])
            else:
                cursor.execute(
                """
                INSERT INTO user_images
                (user_id, data)
                VALUES (%s, %s)
                """,
                [self.id, image])
        else:
            raise AbstractOperationException("User::assign_image()", "user is not persisted")

    def hash_password(self):
        self.password_digest = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


class UserAlreadyActivatedException(Exception):
    """
    Raised when a user object, which is already activated, is invoked to be activated.
    Has no side effects.
    """

    def __init__(self, user_id):
        self.user_id = user_id
