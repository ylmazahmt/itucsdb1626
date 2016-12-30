Parts Implemented by Kerem Er
=============================

This document contains developer's guide information for the features in the application that I implemented.
Content of this document is database design, sql statements for creating and editing information in database, flask codes since application is flask-based and javascript codes used in front-end development of application.

1. `Flask-Based Development`_
	a. `Used Libraries`_
	b. `Route Function Usage`_
2. `Front-End Development`_
	a. `JavaScript Codes`_
	b. `HTML templates`_
2. `Database Design`_
	a. `Chat_Rooms Table`_
	b. `Chat Room Messages Table`_


Flask-Based Development
***************

Used Libraries
---------------
**Used libraries for flask application listed below:**

.. code-block:: python

	import foodle
	import psycopg2
	import bcrypt
	import re
	import jwt
	from psycopg2.extras import RealDictCursor, DictCursor
	from foodle.utils.auth_hook import auth_hook_functor
	from flask import Blueprint, render_template, redirect, current_app, request, make_response, g


Route Function Usage
---------------

**Example usage of defining route function shown below:(Code taken from 'chat_rooms_controller.py')**

.. code-block:: python

chat_rooms_controller = Blueprint('chat_rooms_controller', __name__)
@chat_rooms_controller.route('/',methods=['GET'])
@auth_hook_functor
def index():

**In order to execute a postgresql statement relevant database connection syntax shown below:**

.. code-block:: python

	with psycopg2.connect(foodle.app.config['dsn']) as conn:
		with conn.cursor(cursor_factory=DictCursor) as curs:
			curs.execute("""sql statement""")

**From Flask server function returning a template with variables fetched from database**

.. code-block:: python

return render_template('/chat_rooms/index.html',chat_rooms=chat_rooms,count=count)


Front-End Development
***************

JavaScript Codes
---------------

Chat Rooms
++++++++++

**JavaScipt Function used for add chat room button**

.. code-block:: python

function addChatRoom() {

  const user_id = $('#user_id_input').val()
  const name = $('label.name').children().val()

  $.ajax({
    method: 'POST',
      url: '/chat_rooms/',
      dataType: "json",
      data: JSON.stringify({
        user_id: user_id,
        name: name
      }),
      contentType: 'application/json'
  })
  .always(function (data, textStatus, xhr) {
    window.location.replace('/chat_rooms')
  });
}

**JavaScipt Function used for chat rooms Edit button **

.. code-block:: python

else if(entity === 'chat_room') {
  const name = $('label.name').children().val();

  $.ajax({
    method: 'PUT',
    url: '/chat_rooms/' + identifier,
    data: JSON.stringify({
      name: name
    }),
    contentType: 'application/json'
  })
  .always(function (data, textStatus, xhr) {
    window.location = xhr.getResponseHeader('location');
  });

**JavaScipt Function used for chat rooms Delete button **

.. code-block:: python

else if (entity === 'chat_room') {
  $.ajax({
    method: 'DELETE',
    url: '/chat_rooms/' + identifier
  })
  .success(function (data, textStatus, xhr) {
    alert('Operation completed.')
    window.location.replace('/chat_rooms')
  })
}

Chat Room Messages
++++++++++++++++++

**JavaScipt Function used for add chat room message button**

.. code-block:: python

function addChatRoomMessage() {
  const user_id = $('#user_id_input').val()
  const chat_room_id = $('#chat_room_id_input').val()
  const body = $('label.body').children().val()

  $.ajax({
    method: 'POST',
      url: '/chat_room_messages/',
      dataType: 'json',
      data: JSON.stringify({
        user_id: user_id,
        chat_room_id: chat_room_id,
        body: body
      }),
      contentType: 'application/json'
  })
  .always(function (data, textStatus, xhr) {
    window.location.replace('/chat_room_messages')
  });
}

**JavaScipt Function used for chat room message's edit button**

.. code-block:: python

else if(entity === 'chat_room_message') {
  const body = $('label.body').children().val();

  $.ajax({
    method: 'PUT',
    url: '/chat_room_messages/' + identifier,
    data: JSON.stringify({
      body: body
    }),
    contentType: 'application/json'
  })
  .always(function (data, textStatus, xhr) {
    window.location.replace('../');
  });

**JavaScipt Function used for chat room messages Delete button**

.. code-block:: python

else if (entity === 'chat_room_message') {
  $.ajax({
    method: 'DELETE',
    url: '/chat_room_messages/' + identifier
  })
  .success(function (data, textStatus, xhr) {
    alert('Operation completed.')
    window.location.replace('/chat_room_messages')
  })

HTML Templates
---------------

**For Chat Rooms Page following templates implemented**

	*/foodle/templates/chat_rooms/index.html

  */foodle/templates/chat_rooms/show.html

	*/foodle/templates/chat_rooms/new.html

	*/foodle/templates/chat_rooms/edit.html

**For Chat Room Messages Page following templates implemented**

	*/foodle/templates/chat_room_messages/index.html

	*/foodle/templates/chat_room_messages/show.html

	*/foodle/templates/chat_room_messages/edit.html

	*/foodle/templates/chat_room_messages/new.html


Database Design
***************

Chat Rooms Table
---------------

* 'chat rooms' table keeping records of all chat rooms.

                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | id            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |user_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |name           | text       |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |inserted_at    | timestamp  |   1       |  0        |
                +---------------+------------+-----------+-----------+

* 'user_id' is integer value of corresponding table id which references 'users' table.
* 'name' is text value which contains name of the chat room.
* 'inserted_at' is timestamp value which shows time for creation of instance.

Creating Table
++++++++++++++

**Sql statement that initialize the table**:

.. code-block:: sql

CREATE TABLE chat_rooms(
  id serial PRIMARY KEY,
  user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
  name character varying(255) UNIQUE NOT NULL,
  inserted_at timestamp DEFAULT now() NOT NULL
);

SELECT Operations
+++++++++++++++++

**Sql statement that lists all chat rooms**:

.. code-block:: sql

SELECT cr.id, cr.name, u.username
      FROM chat_rooms as cr
      INNER JOIN users as u ON cr.user_id=u.id
      LIMIT %s
      OFFSET %s
      """,
      [limit, offset])

**Sql statement that shows current chat room**:

.. code-block:: sql

SELECT crm.id, cr.name, crm.body, u.username
      FROM chat_room_messages as crm
      INNER JOIN users as u ON crm.user_id=u.id
      INNER JOIN chat_rooms as cr ON crm.chat_room_id = cr.id
      WHERE crm.chat_room_id=%s
      """,
      [id])

**Sql statement that returns count of  current chat rooms**:

.. code-block:: sql

  SELECT count(id)
        FROM chat_rooms
        """)

**Sql statement that returns messages of a spesific user**:

.. code-block:: sql

SELECT *
        FROM chat_room_messages AS crm
        INNER JOIN users AS u ON u.id = crm.user_id
        WHERE chat_room_id = %s
        LIMIT 10
        """,
        [chat_room['id']])


DELETE Operations
+++++++++++++++++

**Sql statement that deletes chat room from chat rooms table**:

.. code-block:: sql

DELETE FROM chat_rooms
      WHERE id = %s
      """,
      [id])


INSERT Operations
+++++++++++++++++

**Sql statement that inserts new records to the chat rooms table**:

.. code-block:: sql

INSERT INTO chat_rooms
      (user_id, name)
      VALUES (%s, %s)
      RETURNING id
      """,
      [user_id, name])

UPDATE Operations
+++++++++++++++++

**Sql statement that updates existing chat room**:

.. code-block:: sql

UPDATE chat_rooms
      SET name = %s
      WHERE id = %s
      """,
      [name,id])


Chat Room Messages Table
------------------------

* 'chat_room_messages' table keeping records of comments with its related chat_rooms id and owner id

                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | id            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |user_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |chat_room_id   | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |body           | TEXT       |   0       |  0        |
                +---------------+------------+-----------+-----------+
		            |inserted_at    | TIMESTAMP  |   1       |  0        |
                +---------------+------------+-----------+-----------+

* 'user_id' is integer value of corresponding table id which references 'users' table.
* 'check_in_id' is integer value of corresponding table id which references 'check_ins' table.
* 'body' is text value which holds comment content.
* 'inserted_at' timestamp value holds information when tuple added.

Creating Table
++++++++++++++

**Sql statement that initialize the table**:

.. code-block:: sql

CREATE TABLE chat_room_messages(
  id serial PRIMARY KEY,
  user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
  chat_room_id integer NOT NULL REFERENCES chat_rooms(id) ON DELETE CASCADE ON UPDATE CASCADE,
  body text UNIQUE NOT NULL,
  inserted_at timestamp DEFAULT now() NOT NULL
);

SELECT Operations
+++++++++++++++++

**Sql statement that lists all available chat_room_messages in database**:

.. code-block:: sql

SELECT crm.id, cr.name, crm.body, u.username
      FROM chat_room_messages as crm
      INNER JOIN users as u ON crm.user_id=u.id
      INNER JOIN chat_rooms as cr ON crm.chat_room_id = cr.id
      LIMIT %s
      OFFSET %s
      """,
      [limit, offset])

**Sql statement that counts number of chat room messages**:

.. code-block:: sql

SELECT count(id)
      FROM chat_room_messages
      """)

**Sql statement that shows spesific chat room message**:

.. code-block:: sql

SELECT *
      FROM chat_room_messages AS crm
      INNER JOIN users AS u ON u.id=crm.user_id
      WHERE crm.id = %s
      """,
      [id])


**Sql statement that selects user who posted spesific chat room message**:

.. code-block:: sql

SELECT id, username
      FROM users
      """,
      )

**Sql statement that selects chat room which message exits in**:

.. code-block:: sql

SELECT id, name
      FROM chat_rooms
      """,
      )


DELETE Operation
+++++++++++++++++

**Sql statement that used to remove chat room message from database**:

.. code-block:: sql

DELETE FROM chat_room_messages
      WHERE id = %s
      """,
      [id])


INSERT Operation
+++++++++++++++++

**Sql statement that add new tuple to chat_room_messages table **:

.. code-block:: sql

INSERT INTO chat_room_messages
      (user_id, chat_room_id, body)
      VALUES (%s, %s, %s)
      RETURNING id
      """,
      [user_id, chat_room_id, body])

UPDATE Operation
+++++++++++++++++

**Sql statement that update relevant tuple in chat_room_messages tabşe as setting body to new message value:**

.. code-block:: sql

UPDATE chat_room_messages
    SET body = %s
    WHERE id = %s
    """,
    [body,id])
