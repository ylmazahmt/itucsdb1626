Parts Implemented by Ahmet Yılmaz
================================

This document contains developer's guide information for the features in the application that I implemented.
Content of this document is database design, sql statements for creating and editing information in database, flask codes since application is flask-based and javascript codes used in front-end development of application.

1. `Flask-Based Development`_
	a. `Used Libraries`_
	b. `Route Function Usage`_
2. `Front-End Development`_
	a. `JavaScript Codes`_
	b. `HTML templates`_
2. `Database Design`_
	a. `Friendship Table`_
	b. `Check-In Comments Table`_
	c. `Place Ratings Table`_


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

**Example usage of defining route function shown below:(Code taken from 'user_friends_controller.py')**

.. code-block:: py

	user_friends_controller = Blueprint('user_friends_controller', __name__)
	@user_friends_controller.route('/<int:id>/friends/', methods=['GET'])
	@auth_hook_functor
	def index(id):

**In order to execute a postgresql statement relevant database connection syntax shown below:**

.. code-block:: python

	with psycopg2.connect(foodle.app.config['dsn']) as conn:
		with conn.cursor(cursor_factory=DictCursor) as curs:
			curs.execute("""sql statement""")

**From Flask server function returning a template with variables fetched from database**

.. code-block:: python
	
	return render_template('/users/friends/index.html', friends = friends, next="index", pending_request_count = pending_request_count, pending_requests = pending_requests, friend_count = friend_count, current_user = id)


Front-End Development
***************

JavaScript Codes
---------------

Check-In Comments
+++++++++++++++++

**JavaScipt Function used for adding check-in comment button**

.. code-block:: python

	function addComment(entity) {
		if (entity === "check_in_comment") {
		  const message = $('#comment_input').val()
		  const user_id = $('#user_id_input').val()
		  const check_in_id = $('#check_in_id_input').val()

		  $.ajax({
		    method: 'POST',
		    url: '/check_in_comments/',
		    dataType: "json",
		    data: JSON.stringify({
		      body: message,
		      user_id: user_id,
		      check_in_id: check_in_id
		    }),
		    contentType: 'application/json'
		  })
		  .always(function (data, textStatus, xhr) {
		    window.location.replace('/check_in_comments')
		  });
		}
	}

**JavaScipt Function used for edit check-in comment button**

.. code-block:: python

	if (entity === 'check_in_comment') {
	    const message = $('#comment_edit').val()

	    $.ajax({
	      method: 'PUT',
	      url: '/check_in_comments/' + identifier,
	      data: JSON.stringify({
		body: message
	      }),
	      contentType: 'application/json'
	    })
	    .always(function (data, textStatus, xhr) {
	      window.location = xhr.getResponseHeader('location')
	    });
	}
	    
**JavaScipt Function used for delete check-in comment button**

.. code-block:: python

	if (entity === 'check_in_comment') {
	    $.ajax({
	      method: 'DELETE',
	      url: '/check_in_comments/' + identifier
	    })
	    .success(function (data, textStatus, xhr) {
	      alert('Operation completed.')
	      window.location.replace('/check_in_comments')
	    })
	}

Place Ratings
+++++++++++++

**JavaScipt Function used for add place rating button**

.. code-block:: python

	function addRating() {
		const rating = $('#rating_input').val()
		const user_id = $('#user_id_input').val()
		const place_id = $('#place_id_input').val()

		$.ajax({
			method: 'POST',
		    url: '/place_ratings/',
		    dataType: "json",
		    data: JSON.stringify({
			rating: rating,
			user_id: user_id,
			place_id: place_id
		    }),
		    contentType: 'application/json'
		})
		.always(function (data, textStatus, xhr) {
	    window.location.replace('/place_ratings')
		});
	}

**JavaScipt Function used for edit place rating button**

.. code-block:: python

	if (entity === 'place_rating') {
	    const rating = $('#rating_edit').val()

	    $.ajax({
	      method: 'PUT',
	      url: '/place_ratings/' + identifier,
	      data: JSON.stringify({
		rating: rating
	      }),
	      contentType: 'application/json'
	    })
	    .always(function (data, textStatus, xhr) {
	      window.location = xhr.getResponseHeader('location')
	    });
	}
	    
**JavaScipt Function used for delete place rating button**

.. code-block:: python

	if (entity === 'place_rating') {
	    $.ajax({
	      method: 'DELETE',
	      url: '/place_ratings/' + identifier
	    })
	    .success(function (data, textStatus, xhr) {
	      alert('Operation completed.')
	      window.location.replace('/place_ratings')
	    })
	  }

HTML Templates
---------------

**For Friends Page following templates implemented**

	*/foodle/templates/users/friends/index.html
	
	*/foodle/templates/users/friends/new_friend.html
	
	*/foodle/templates/users/friends/requests_index.html
	
**For Check-In Comments Page following templates implemented**

	*/foodle/templates/check_in_comments/index.html
	
	*/foodle/templates/check_in_comments/show.html
	
	*/foodle/templates/check_in_comments/edit.html
	
	*/foodle/templates/check_in_comments/new.html
	
**For Place Ratings Page following templates implemented**

	*/foodle/templates/place_ratings/index.html
	
	*/foodle/templates/place_ratings/show.html
	
	*/foodle/templates/place_ratings/edit.html
	
	*/foodle/templates/place_ratings/new.html
	

Database Design
***************

Friendship Table
---------------

* 'user_friends' table keeping records of all user relations between each other.

                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | id            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |user_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |friend_id      | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |is_friend      | BOOLEAN    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                
* 'user_id' is integer value of corresponding table id which references 'users' table.
* 'friend_id' is integer value of corresponding table id which references 'users' table.
* 'is_friend' is boolean value which is true if two users in same tuple is recognized as friends, false otherwise.

Notes
+++++

**Some notation for values used in postgresql statements:**

* id = user id that current session owner has fetched from users table.
* second_user_id = selected user to use in table operation as second user related to current user.
* string_to_search = keyword for search feature used.

Creating Table
++++++++++++++

**Sql statement that initialize the table**:

.. code-block:: sql

   CREATE TABLE user_friends(
      id serial PRIMARY KEY,
      user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
      friend_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
      is_friend boolean NOT NULL
  );
  
SELECT Operations
+++++++++++++++++

**Sql statement that lists all friends of current user**:

.. code-block:: sql

	SELECT u.id, u.username, u.display_name, ui.url, u.inserted_at
	FROM user_friends AS uf
	INNER JOIN users AS u ON u.id = uf.friend_id
	INNER JOIN user_images AS ui ON ui.user_id = u.id
	WHERE uf.user_id = %s
	AND uf.is_friend = TRUE
	LIMIT %s
	OFFSET %s
	,
	[id, limit, offset]
              
**Sql statement that lists all friend requests that current user sent**:

.. code-block:: sql

	SELECT u.id, count(u.id) prc, u.username, u.display_name, ui.url, u.inserted_at
	FROM user_friends AS uf
	INNER JOIN users AS u ON u.id = uf.friend_id
	INNER JOIN user_images AS ui ON ui.user_id = u.id
	WHERE uf.user_id = %s
	AND uf.is_friend = FALSE
	GROUP BY u.id, ui.url
	,
	[id]

**Sql statement that lists all friend requests that current user received from other users**:

.. code-block:: sql

	SELECT u.id, u.username, u.display_name, ui.url, u.inserted_at
       	FROM user_friends AS uf
        INNER JOIN users AS u ON u.id = uf.user_id
        INNER JOIN user_images AS ui ON ui.user_id = u.id
        WHERE uf.friend_id = %s AND uf.is_friend = FALSE
        LIMIT %s
        OFFSET %s
        ,
        [id, limit, offset]

**Sql statement that lists all friends of current user from database upon request with a keyword search**:

.. code-block:: sql

	SELECT u.id,count(u.id), u.username, u.display_name, ui.url, u.inserted_at
	FROM user_friends AS uf
	INNER JOIN users AS u ON u.id = uf.friend_id
	INNER JOIN user_images AS ui ON ui.user_id = u.id
	WHERE uf.user_id = %s
	AND (u.display_name ILIKE %s OR u.username ILIKE %s ESCAPE '=')
	AND uf.is_friend = TRUE
	GROUP BY u.id, ui.url
	LIMIT %s
	OFFSET %s
	,
	[id,'%' + string_to_search + '%', '%' + string_to_search + '%', limit, offset]

**Sql statement that lists all friend requests that current user sent from database upon request with a keyword search**:

.. code-block:: sql

	SELECT u.id,count(u.id) prc, u.username, u.display_name, ui.url, u.inserted_at
	FROM user_friends AS uf
	INNER JOIN users AS u ON u.id = uf.friend_id
	INNER JOIN user_images AS ui ON ui.user_id = u.id
	WHERE uf.user_id = %s
	AND (u.display_name ILIKE %s OR u.username ILIKE %s ESCAPE '=')
	AND uf.is_friend = FALSE
	GROUP BY u.id, ui.url
	,
	[id,'%' + string_to_search + '%', '%' + string_to_search + '%']
	
**Sql statement that lists all users which have is total stranger to current user(not friend, no request available between each other)**:

.. code-block:: sql

	SELECT u.id, u.username, u.display_name, u.inserted_at, ui.url
	FROM users u, user_friends uf, user_images ui
	WHERE u.id = ui.user_id AND u.id != %s
	EXCEPT
	SELECT u.id, u.username, u.display_name, u.inserted_at, ui.url
	FROM user_friends AS uf, users AS u 
	INNER JOIN user_images AS ui ON ui.user_id = u.id
	WHERE (uf.user_id = %s AND u.id = uf.friend_id)
	OR  (uf.friend_id =%s AND u.id = uf.user_id)
	LIMIT %s
	OFFSET %s
	,
	[id, id, id, limit, offset]

DELETE Operations
+++++++++++++++++

**Sql statement that remove tuple from table which refers to 'remove friend'**:

.. code-block:: sql

	DELETE FROM user_friends
	WHERE (user_id = %s
	AND friend_id = %s
	AND is_friend)
	OR (user_id = %s
	AND friend_id = %s
	AND is_friend)
	,
	[id, second_user_id, second_user_id, id]

**Sql statement that remove friend request that previously sent by current user whihc refers to 'cancel friend request'**:

.. code-block:: sql

	DELETE FROM user_friends
	WHERE user_id = %s
	AND friend_id = %s
	AND is_friend = False
	,
	[id, second_user_id]

INSERT Operations
+++++++++++++++++

**Sql statement that add new tuple to table with current user and selected user which refers to 'send friend request'**:

.. code-block:: sql

	INSERT INTO user_friends
	(user_id, friend_id, is_friend)
	VALUES(%s, %s, False)
	,
	[id, request_id]
	
**Sql statement that add new tuple to table with current user and selected user which refers to 'accept friend request'**:

.. code-block:: sql

	INSERT INTO user_friends
	(user_id, friend_id, is_friend)
	VALUES(%s, %s, True)
	,
	[id, second_user_id]

UPDATE Operations
+++++++++++++++++

**Sql statement that update relevant tuple as setting is_friend to 'True' upon accepting friend request which means now they are friend**:

.. code-block:: sql

	UPDATE user_friends
	SET is_friend = True
	WHERE user_id = %s
	AND friend_id = %s
	,
	[second_user_id, id]


Check-In Comments Table
---------------

* 'check_in_comments' table keeping records of comments with its related check-in id and owner id

                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | id            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |user_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |check_in_id    | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |body           | TEXT       |   0       |  0        |
                +---------------+------------+-----------+-----------+
		|inserted_at    | TIMESTAMP  |   1       |  0        |
                +---------------+------------+-----------+-----------+
                
* 'user_id' is integer value of corresponding table id which references 'users' table.
* 'check_in_id' is integer value of corresponding table id which references 'check_ins' table.
* 'body' is text value which holds comment content.
* 'inserted_at' timestamp value holds information when tuple added.

Notes
+++++

**Some notation for values used in postgresql statements:**

* id or user_id = user id that current session owner has fetched from users table.
* check_in_id = selected check-in to use in table operation as check_in_id.
* body = comment content to add or edit.

Creating Table
++++++++++++++

**Sql statement that initialize the table**:

.. code-block:: sql

	CREATE TABLE check_in_comments(
	    id serial PRIMARY KEY,
	    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
	    check_in_id integer NOT NULL REFERENCES check_ins(id) ON DELETE CASCADE ON UPDATE CASCADE,
	    body text,
	    inserted_at timestamp DEFAULT now() NOT NULL
	);
  
SELECT Operations
+++++++++++++++++

**Sql statement that lists all available check-in comments in database**:

.. code-block:: sql

	SELECT cic.id, u.username, cic.check_in_id, cic.body
        FROM check_in_comments AS cic
        INNER JOIN users AS u ON cic.user_id = u.id
              
**Sql statement that shows single check-in comment**:

.. code-block:: sql

	SELECT *
        FROM check_in_comments
        WHERE id = %s
        ,
        [id]

**Sql statement that lists all user into selection box for using to comment as user**:

.. code-block:: sql

	SELECT id, username, inserted_at
        FROM users
        

**Sql statement that lists all check-ins into selection box for using for commenting about**:

.. code-block:: sql

	SELECT ci.id, u.display_name, p.name
        FROM check_ins AS ci 
        INNER JOIN users AS u ON ci.user_id = u.id
        INNER JOIN places AS p ON ci.place_id = p.id



DELETE Operation
+++++++++++++++++

**Sql statement that used to remove check-in comment from database**:

.. code-block:: sql

	 DELETE FROM check_in_comments
         WHERE id = %s
         ,
         [id]


INSERT Operation
+++++++++++++++++

**Sql statement that add new tuple to table with informations user, check-in and body**:

.. code-block:: sql

	INSERT INTO check_in_comments
        (user_id, check_in_id, body)
        VALUES (%s, %s, %s)
        RETURNING id
        ,
        [user_id, check_in_id, body]
	

UPDATE Operation
+++++++++++++++++

**Sql statement that update relevant tuple as setting body to new comment value:**

.. code-block:: sql

	UPDATE check_in_comments
        SET body = %s
        WHERE id = %s
        ,
	[body, id]


Place Ratings Table
---------------


* 'place_ratings' table keeping records of all place ratings with its related place id and its owner id.

                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | id            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |user_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |place _id      | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |rating         | INTEGER    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |inserted_at    | TIMESTAMP  |   1       |  0        |
                +---------------+------------+-----------+-----------+
                
                
* 'user_id' is integer value of corresponding table id which references 'users' table.
* 'place_id' is integer value of corresponding table id which references 'places' table.
* 'rating' is integer value corresponds to place rated as by a user.
* 'inserted_at' timestamp value holds information when tuple added.

Notes
+++++

**Some notation for values used in postgresql statements:**

* id or user_id = user id that current session owner has fetched from users table.
* place_id = selected place to use in table operation as place_id.
* rating = rating value to add or edit.

Creating Table
++++++++++++++

**Sql statement that initialize the table**:

.. code-block:: sql

	CREATE TABLE place_ratings(
	    id serial PRIMARY KEY,
	    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
	    place_id integer NOT NULL REFERENCES places(id) ON DELETE CASCADE ON UPDATE CASCADE,
	    rating int,
	    inserted_at timestamp DEFAULT now() NOT NULL
	);
  
SELECT Operations
+++++++++++++++++

**Sql statement that lists all available place ratings in database**:

.. code-block:: sql

	SELECT pr.id, u.username, pr.place_id, p.name, pr.rating
        FROM place_ratings AS pr
        INNER JOIN users AS u ON pr.user_id = u.id
        INNER JOIN places AS p ON pr.place_id = p.id
              
**Sql statement that shows single place rating**:

.. code-block:: sql

	SELECT *
        FROM place_ratings
        WHERE id = %s
        ,
        [id]

**Sql statement that lists all user into selection box for using to rate as user**:

.. code-block:: sql

	SELECT id, username, inserted_at
        FROM users
        

**Sql statement that lists all places into selection box for using to rate to**:

.. code-block:: sql

	SELECT id,name
        FROM places 


DELETE Operation
+++++++++++++++++

**Sql statement that used to remove place rating from database**:

.. code-block:: sql

	 DELETE FROM place_ratings
         WHERE id = %s
         ,
         [id]


INSERT Operation
+++++++++++++++++

**Sql statement that add new tuple to table with informations user, place and rating**:

.. code-block:: sql

	INSERT INTO place_ratings
        (user_id, place_id, rating)
        VALUES (%s, %s, %s)
        RETURNING id
        ,
        [user_id, place_id, rating]
	

UPDATE Operation
+++++++++++++++++

**Sql statement that update relevant tuple as setting rating to new rating value:**

.. code-block:: sql

	UPDATE place_ratings
        SET rating = %s 
        WHERE id = %s
        , 
        [rating, id]


