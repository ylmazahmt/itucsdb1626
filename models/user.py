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
        self.password = password
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

        if not self._persisted:
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

    def friends(self, limit=20, offset=0):
        """
        Fetches friends list of the user.
        """

        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT u.id, u.username, u.email, u.inserted_at
        FROM user_friends AS uf
        INNER JOIN users AS u ON u.id = uf.friend_id
        WHERE uf.user_id = %s
        LIMIT %s
        OFFSET %s
        """,
        [self.id, limit, offset])

        objects = cursor.fetchall()
        friends = []

        for each_object in objects:
            friend = User(each_object[1], None, each_object[2], True)
            friend.id = each_object[0]
            friend.inserted_at = each_object[3]
            friends.append(friend)

        return friends

    def count_friends(self):
        """
        Performs a count query and returns the number of friends
        of a user.
        """

        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT count(uf.id)
        FROM user_friends AS uf
        INNER JOIN users AS u ON u.id = uf.friend_id
        WHERE uf.user_id = %s AND uf.is_friend = TRUE
        """,
        [self.id])

        count = cursor.fetchone()[0]
        db.connection.commit()

        return count

    def pending_requests(self, limit=20, offset=0):

        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT u.id, u.username, u.email, u.inserted_at
        FROM user_friends AS uf
        INNER JOIN users AS u ON u.id = uf.friend_id
        WHERE uf.user_id = %s AND uf.is_friend = FALSE
        LIMIT %s
        OFFSET %s
        """,
        [self.id, limit, offset])

        objects = cursor.fetchall()
        requests = []

        for each_object in objects:
            request = User(each_object[1], None, each_object[2], True)
            request.id = each_object[0]
            request.inserted_at = each_object[3]
            requests.append(request)

        return requests

    def count_requests(self):
        """
        Performs a count query and returns the number of
        pending requests of the user.
        """

        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT count(uf.id)
        FROM user_friends AS uf
        INNER JOIN users AS u ON u.id = uf.friend_id
        WHERE uf.user_id = %s AND uf.is_friend = FALSE
        """,
        [self.id])

        count = cursor.fetchone()[0]
        db.connection.commit()

        return count


    def is_friend_or_pending(self, second_user):

        # value = 3, friend request sent
        # value = 2, friend
        # value = 1, pending request
        # value = 0, total stranger

        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT user_id
        FROM user_friends
        WHERE (user_id = %s
        AND friend_id = %s)
        OR (user_id = %s
        AND friend_id = %s);
        """,
        [self.id, second_user.id, second_user.id, self.id])

        data = cursor.fetchall()

        if len(data) == 1:
            if data[0][0] == self.id:
                return 3
            else:
                return 1
        else:
            return len(data) # 0 or 2

    def add_friend(self, second_user):
        """
        add or update relevant relationship information about two given users
        """
        relationship = self.is_friend_or_pending(second_user)

        if relationship == 2 or relationship == 3:
            return False

        cursor = db.connection.cursor()

        #send friend request
        if relationship == 0:
            cursor.execute(
            """
            INSERT INTO user_friends
            (user_id, friend_id, is_friend)
            VALUES(%s, %s, False)
            """,
            [self.id, second_user.id])


        #accept the friend request
        elif relationship == 1:
            cursor.execute(
            """
            INSERT INTO user_friends
            (user_id, friend_id, is_friend)
            VALUES(%s, %s, True)
            """,
            [self.id, second_user.id])

            cursor.execute(
            """
            UPDATE user_friends
            SET is_friend = True
            WHERE user_id = %s
            AND friend_id = %s
            """,
            [second_user.id, self.id])

        db.connection.commit()

        return True

    def find_in_friends(self, str_s, limit=20, offset=0):
        #fetch all friends of given user
        cursor = db.connection.cursor()

        cursor.execute(
        """
        SELECT username, friend_id
        FROM user_friends,users
        WHERE friend_id = users.id
        AND user_id = '%s'
        AND username LIKE '%s'
        AND is_friend
        LIMIT %s
        OFFSET %s
        """,
        [self.id, str_s, limit, offset])

        objects = cursor.fetchall()

        friends = []

        for each_object in objects:
            friend = User.get_user(each_object[1])
            friends.append(friend)

        return friends

    def remove_friend(first_user, second_user):
        #delete friendship about two given users from database
        cursor = db.connection.cursor()

        cursor.execute(
        """
        DELETE FROM user_friends
        WHERE (user_id = %s
        AND friend_id = %s
        AND is_friend)
        OR (user_id = %s
        AND friend_id = %s
        AND is_friend)
        """,
        [first_user.id, second_user.id, second_user.id, first_user.id])

        db.connection.commit()

        return True


class UserAlreadyActivatedException(Exception):
    """
    Raised when a user object, which is already activated, is invoked to be activated.
    Has no side effects.
    """

    def __init__(self, user_id):
        self.user_id = user_id
