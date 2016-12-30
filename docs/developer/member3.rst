Parts Implemented by Ali Rıza Salihoğlu
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

**Example usage of defining route function shown below:(Code taken from 'cities_controller.py')**

.. code-block:: py


cities_controller = Blueprint('cities_controller',__name__)

@cities_controller.route('/',methods=['GET'])
@auth_hook_functor
def index():

**In order to execute a postgresql statement relevant database connection syntax shown below:**

.. code-block:: python

	with psycopg2.connect(foodle.app.config['dsn']) as conn:
		with conn.cursor(cursor_factory=DictCursor) as curs:
			curs.execute("""sql statement""")

**From Flask server function returning a template with variables fetched from database**

.. code-block:: python

	return render_template('/cities/index.html', cities=cities,count=count)


Front-End Development
***************

JavaScript Codes
---------------

Cities
+++++++++++++++++

**JavaScipt Function used for adding city button**

.. code-block:: python

	function addCity() {

			const user_id = $('#user_id_input').val()
			const name = $('label.name').children().val()
			const description = $('label.description').children().val()
			$.ajax({
				method: 'POST',
					url: '/cities/',
					dataType: "json",
					data: JSON.stringify({
						user_id: user_id,
						name: name,
						description: description
					}),
					contentType: 'application/json'
			})
			.always(function (data, textStatus, xhr) {
				window.location.replace('/cities')
			});
	}

**JavaScipt Function used for edit city button**

.. code-block:: python

	if (entity === 'city') {
		const name = $('label.name').children().val();
		const description = $('label.description').children().val();

		$.ajax({
			method: 'PUT',
			url: '/cities/' + identifier,
			data: JSON.stringify({
				name: name,
				description: description
			}),
			contentType: 'application/json'
		})
		.always(function (data, textStatus, xhr) {
			window.location = xhr.getResponseHeader('location');
		});
	}

**JavaScipt Function used for delete city button**

.. code-block:: python

	if (entity === 'city') {
		$.ajax({
			method: 'DELETE',
			url: '/cities/' + identifier
		})
		.success(function (data, textStatus, xhr) {
			alert('Operation completed.')
			window.location.replace('/cities')
		})

	}

Places
+++++++++++++

**JavaScipt Function used for add place button**

.. code-block:: python

	function addPlace() {
		const user_id = $('#user_id_input').val();
		const name = $('label.name').children().val();
		const description = $('label.description').children().val();

		$.ajax({
			method: 'POST',
				url: '/places/',
				dataType: "json",
				data: JSON.stringify({
					user_id: user_id,
					name: name,
					description: description
				}),
				contentType: 'application/json'
		})
		.always(function (data, textStatus, xhr) {
			window.location.replace('/places')
		});

	}

**JavaScipt Function used for edit place button**

.. code-block:: python

	if(entity === 'place') {
		const name = $('label.name').children().val()
		const description = $('label.description').children().val()

		$.ajax({
			method: 'PUT',
			url: '/places/' + identifier,
			data: JSON.stringify({
				name: name,
				description: description
			}),
			contentType: 'application/json'
		})
		.always(function (data, textStatus, xhr) {
			window.location.replace('../');
		});
	}

**JavaScipt Function used for delete place button**

.. code-block:: python

	if (entity === 'place') {

		$.ajax({
			method: 'DELETE',
			url: '/places/' + identifier
		})
		.success(function (data, textStatus, xhr) {
			alert('Operation completed.')
			window.location.replace('/places')
		})

	}

	Place Instances
	+++++++++++++

	**JavaScipt Function used for add place button**

	.. code-block:: python

		function addPlaceInstance() {
			const user_id = $('#user_id_input').val();
			const place_id = $('#place_id_input').val();
			const city_id = $('#city_id_input').val();
			const name = $('label.name').children().val();
			const address = $('label.address').children().val();
			const capacity = $('label.capacity').children().val();

			$.ajax({
				method: 'POST',
				url: '/place_instances/',
				dataType: "json",
				data: JSON.stringify({
					user_id: user_id,
					place_id: place_id,
					city_id: city_id,
					name: name,
					address: address,
					capacity: capacity
				}),
				contentType: 'application/json'
			})
			.always(function (data, textStatus, xhr) {
				window.location.replace('/place_instances')
			});
		}

	**JavaScipt Function used for edit place instance button**

	.. code-block:: python

		if(entity === 'place_instances') {
		 const name = $('label.name').children().val()
		 const address = $('label.address').children().val()
		 const capacity = $('label.capacity').children().val()

		 $.ajax({
			 method: 'PUT',
			 url: '/place_instances/' + identifier,
			 data: JSON.stringify({
				 name: name,
				 address: address,
				 capacity: capacity
			 }),
			 contentType: 'application/json'
		 })
		 .always(function (data, textStatus, xhr) {
			 window.location.replace('../');
		 });
	 }

	**JavaScipt Function used for delete place button**

	.. code-block:: python

		if (entity === 'place_instance') {

			$.ajax({
				method: 'DELETE',
				url: '/place_instances/' + identifier
			})
			.success(function (data, textStatus, xhr) {
				alert('Operation completed.')
				window.location.replace('/place_instances')
			})

		}

HTML Templates
---------------

**For Cities Page following templates implemented**

	*/foodle/templates/users/cities/index.html

	*/foodle/templates/users/cities/show.html

	*/foodle/templates/users/cities/new.html

	*/foodle/templates/users/cities/edit.html


**For Places Comments Page following templates implemented**

	*/foodle/templates/users/places/index.html

	*/foodle/templates/users/places/show.html

	*/foodle/templates/users/places/new.html

	*/foodle/templates/users/places/edit.html

**For Place Instances Page following templates implemented**

	*/foodle/templates/users/place_instances/index.html

	*/foodle/templates/users/place_instances/show.html

	*/foodle/templates/users/place_instances/new.html

	*/foodle/templates/users/place_instances/edit.html


Database Design
***************

Cities Table
---------------

* 'cities' table keeping records of cities.

                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | id            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |user_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |name			      | VARCHAR    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |description 	  | text   		 |   1       |  0        |
                +---------------+------------+-----------+-----------+

* 'user_id' is an integer value of corresponding table id which references 'users' table.
* 'name' is a varchar  which holds the name of the city.
* 'description' is a text  which holds the description of the city.

Notes
+++++

**Some notation for values used in postgresql statements:**

* id = user id that current session owner has fetched from users table.

Creating Table
++++++++++++++

**Sql statement that initialize the table**:

.. code-block:: sql

	CREATE TABLE cities(
		id serial PRIMARY KEY,
		user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
		name character varying(255) UNIQUE NOT NULL,
		description text NOT NULL
	);

SELECT Operations
+++++++++++++++++

**Sql statement that lists all cities**:

.. code-block:: sql

			SELECT c.id, c.name, c.description, u.username
			FROM cities as c
			INNER JOIN users as u ON c.user_id=u.id
			LIMIT %s
			OFFSET %s
			,
			[limit, offset]


**Sql statement that lists all  place instances that under a specific city**:

.. code-block:: sql

				SELECT *
				FROM place_instances
				WHERE city_id = %s
				LIMIT 10
				,
				[city['id']]

**Sql statement that shows selected city **:

.. code-block:: sql

				SELECT id, name, description
				FROM cities
				WHERE id = %s
				,
				[id]

DELETE Operations
+++++++++++++++++

**Sql statement that remove tuple from table which refers to 'delete city'**:

.. code-block:: sql

				DELETE FROM cities
				WHERE id = %s
				,
				[id]


INSERT Operations
+++++++++++++++++

**Sql statement that add new tuple to table with current user and given name and description which refers to 'add city'**:

.. code-block:: sql

			INSERT INTO cities
			(user_id, name, description)
			VALUES (%s, %s, %s)
			RETURNING id
			,
			[user_id, name, description]


UPDATE Operations
+++++++++++++++++

**Sql statement that update relevant tuple as whith given name and description**:

.. code-block:: sql

			UPDATE cities
			SET name = %s , description = %s
			WHERE id = %s
			,
			[name, description, id]


Places Table
---------------

* 'Places' table keeping records of places.

                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | id            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |user_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |name				    | VARCHAR    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |description    | TEXT       |   1       |  0        |
                +---------------+------------+-----------+-----------+
								|inserted_at    | TIMESTAMP  |   1       |  0        |
                +---------------+------------+-----------+-----------+

* 'user_id' is an integer value of corresponding table id which references 'users' table.
* 'name' is a varchar which holds the place name.
* 'description' is text value which holds description of the place.
* 'inserted_at' timestamp value holds information when tuple added.

Notes
+++++

**Some notation for values used in postgresql statements:**

* id or user_id = user id that current session owner has fetched from users table.

Creating Table
++++++++++++++

**Sql statement that initialize the table**:

.. code-block:: sql

	CREATE TABLE places(
	    id serial PRIMARY KEY,
	    description text NOT NULL,
	    name character varying(255) UNIQUE NOT NULL,
	    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
	    inserted_at timestamp DEFAULT now() NOT NULL
	);

SELECT Operations
+++++++++++++++++

**Sql statement that lists all places in database**:

.. code-block:: sql

				SELECT p.name, p.id, p.description, u.username
				FROM places as p
				INNER JOIN users as u ON p.user_id=u.id
				LIMIT %s
				OFFSET %s
				,
				[limit, offset]

	**Sql statement that counts all places in database**:

.. code-block:: sql
				SELECT count(*)
				FROM places

**Sql statement that shows selected place**:

.. code-block:: sql

			SELECT *
			FROM places
			WHERE id = %s
			,
			[id]



DELETE Operation
+++++++++++++++++

**Sql statement that used to remove a city  from database**:

.. code-block:: sql

			DELETE FROM places
			WHERE id = %s
			, [id]


INSERT Operation
+++++++++++++++++

**Sql statement that add new tuple to table with informations user, name-in and description**:

.. code-block:: sql

			INSERT INTO places
			(name, description, user_id)
			VALUES (%s, %s, %s)
			RETURNING id
			,
			[name, description, user_id]


UPDATE Operation
+++++++++++++++++

**Sql statement that update relevant tuple as setting description and name to new values**

.. code-block:: sql

			UPDATE places
			SET name = %s , description = %s
			WHERE id = %s
			,
			[name, description, id]

Place Instances Table
---------------


* 'place_instances' table keeping records of all place instances.

                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | id            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |user_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |place _id      | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |city_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
								|name     		  | VARCHAR  	 |   1       |  0        |
								+---------------+------------+-----------+-----------+
								|address        | TEXT  		 |   1       |  0        |
								+---------------+------------+-----------+-----------+
								|capacity       | VARCHAR    |   1       |  0        |
								+---------------+------------+-----------+-----------+
                |inserted_at    | TIMESTAMP  |   1       |  0        |
                +---------------+------------+-----------+-----------+


* 'user_id' is an integer value of corresponding table id which references 'users' table.
* 'place_id' is an integer value of corresponding table id which references 'places' table.
* 'city_id' is an integer value of corresponding table id which references 'cities' table.
* 'name' is a varchar value corresponds to place instance name.
* 'address' is a text value corresponds to place instance address.
* 'capacity' is a varchar value corresponds to place instance capacity.
* 'inserted_at' timestamp value holds information when tuple added.

Notes
+++++

**Some notation for values used in postgresql statements:**

* id or user_id = user id that current session owner has fetched from users table.
* place_id = selected place to use in table operation as place_id.
* city_id = selected place to use in table operation as city_id.

Creating Table
++++++++++++++

**Sql statement that initialize the table**:

.. code-block:: sql

	CREATE TABLE place_instances(
			id serial PRIMARY KEY,
			city_id integer NOT NULL REFERENCES cities(id) ON DELETE CASCADE ON UPDATE CASCADE,
			user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
			place_id integer NOT NULL REFERENCES places(id) ON DELETE CASCADE ON UPDATE CASCADE,
			name character varying(255) UNIQUE NOT NULL,
			address text NOT NULL,
			capacity character varying(255) NOT NULL,
			inserted_at timestamp DEFAULT now() NOT NULL
	);

SELECT Operations
+++++++++++++++++

**Sql statement that lists all available place instances in database**:

.. code-block:: sql

			SELECT *
			FROM place_instances
			LIMIT %s
			OFFSET %s
			,
			[limit, offset]

**Sql statement that counts all available place instances in database**:

.. code-block:: sql

			SELECT count(id)
			FROM place_instances


**Sql statement that shows single place instance**:

.. code-block:: sql

			SELECT *
			FROM place_instances
			WHERE id = %s
			,
			[id]

**Sql statement that lists all place instances in a place**:

.. code-block:: sql

"""
			SELECT *
			FROM place_instances
			WHERE place_id = %s
			LIMIT 10
			,
			[place['id']]


**Sql statement that lists all plac instances in a city**:

.. code-block:: sql

			SELECT *
			FROM place_instances
			WHERE city_id = %s
			LIMIT 10
			,
			[city['id']])

DELETE Operation
+++++++++++++++++

**Sql statement that used to remove place instance from database**:

.. code-block:: sql

			DELETE FROM place_instances
			WHERE id = %s
			, [id]


INSERT Operation
+++++++++++++++++

**Sql statement that add new tuple to table with informations user, place, city, name, address and capacity**:

.. code-block:: sql

		INSERT INTO place_instances
		(name, user_id, place_id, capacity, city_id, address)
		VALUES (%s, %s, %s, %s, %s, %s)
		RETURNING id
		,
		[name, user_id, place_id, capacity, city_id, address]


UPDATE Operation
+++++++++++++++++

**Sql statement that update relevant tuple as setting name, capacity and address to new values:**

.. code-block:: sql

		UPDATE place_instances
			SET name = %s,
					capacity = %s,
					address = %s
			WHERE id = %s
			,
			[name, capacity, address, id]
