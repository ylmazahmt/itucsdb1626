import bcrypt
import psycopg2
from middleware import db
from models.error_handling import AbstractOperationException

class User:
    """
    The user model class representing users of the application.
    """


    def __init__(self, username, password, email, persisted=False):
        """
        Initializes a new instance of user.
        """

        self.id = None
        self.username = username
        self.password_digest = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.email = email
        self._persisted = persisted


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
            raise AbstractOperationException("User::activate()", "user is not persisted")


class UserAlreadyActivatedException(Exception):
    """
    Raised when a user object, which is already activated, is invoked to be activated.
    Has no side effects.
    """

    def __init__(self, user_id):
        self.user_id = user_id
