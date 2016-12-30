Parts Implemented by Buğra Ekuklu
================================

This document consists of development information about user and post entities and client-side. User is special kind of entity which affects the authentication-authorization process.

1. `RESTful Design`_
  a. `Stateless Design`_
  b. `Session vs. Token Authentication`_
2. `Client-side Development`_
3. `Route Registration`_
4. `Database Instantiation and Seeding`
5. `Users API`_
6. `Feed API`_
7. `Posts API`_
8. `Search Bar`_

RESTful Design
**************

REST refers to **Representational State Transfer**, which is defined by the Roy Fielding in his dissertation. The technique could be implemented on top of `HTTP` application OSI layer in order to make *RPC-y* communication more intuitive. An entity could be interfaced with corresponding HTTP API with following actions:

  * `:index`: Lists all users.
    `GET /users`
  * `:show`: Shows a user with identifier.
    `GET /users/27`
  * `:create`: Creates a new user with given parameters included in request payload.
    `POST /users`
  * `:update`: Updates an existing user with given identifier by replacing that user with given parameters included in request payload.
    `PUT /users/27`
  * `:delete`: Deletes an existing user with given identifier.
    `DELETE /users/27`

It is highly recommended to use a wide collection of *HTTP status codes* in order to give more information which is more predicable, to the consumer of the API.

Stateless Design
----------------

An API augmented with REST should be stateless in order to scale horizontally. Therefore every operation invoked by a remote procedure caller, in this case client-side of the application, should be atomic. This affected the database calls made by server-side, if there is more than one query, they should be run in proper transaction/locking rules.

Session vs. Token Authentication
--------------------------------

Session based authentication is a traditional technique of storing state of the client, generally about authentication of the client user. Sessions are held by `HttpOnly` cookies on the browser, however this creates a problem in scaling since server needs to fetch the user authenticated in each HTTP request.

Tokens (in our case, they're JSON Web Tokens) are self-contained, meaning they contain information of the client. They could not be changed by the client since they also contain `HS*` or `RS*` signatures, which is generated in server using its secret key. Tokens augment stateless authentication since they could be decoded by the server on each request. We used `localStorage` property of the browser, which is an `HTML5` feature.

Since tokens are stored in `localStorage`, they are immune to **CSRF** (cross-site request forgery).

The decorator we used to make authentication as pre-hook on Flask routes is implemented like so:

  .. code-block:: python

    def auth_hook_functor(fn):
        @wraps(fn)
        def decorated_fn(*args, **kwargs):
            token = request.cookies.get('jwt')

            if token is None:
                return redirect('/sessions/new')
            else:
                try:
                    g.current_user = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])
                except:
                    return redirect('/sessions/new')

                return fn(*args, **kwargs)
        return decorated_fn

Client-side Development
***********************

We used plain-old vanilla Javascript in our client-side code. Since sometimes we used `fetch`, we used `whatwg-fetch` polyfill to support old browsers.

We also used some external libraries like `lodash` to write functional Javascript, `moment.js` to make timestamps human-readable and `jQuery` to edit DOM content and make XHR requests.

Route Registration
******************

We used *-VC* (view-controller) design pattern in order to seperate data based operations and markup renderings. Each controller is a Flask blueprint. They are added as routes in application router, which is `router.py`.

  .. code-block:: python

    def bootstrap():
        app.register_blueprint(application_controller)
        app.register_blueprint(users_controller, url_prefix='/users')
        app.register_blueprint(user_user_activation_controller, url_prefix='/users')
        app.register_blueprint(session_controller, url_prefix='/sessions')
        app.register_blueprint(feed_controller, url_prefix='/users')
        app.register_blueprint(user_friends_controller, url_prefix='/users')
        app.register_blueprint(user_friend_requests_controller, url_prefix='/users')
        app.register_blueprint(places_controller, url_prefix='/places')
        app.register_blueprint(place_instances_controller, url_prefix='/place_instances')
        app.register_blueprint(posts_controller, url_prefix='/posts')
        app.register_blueprint(check_ins_controller, url_prefix='/check_ins')
        app.register_blueprint(database_initialization_controller, url_prefix='/database_initialization')
        app.register_blueprint(post_comments_controller, url_prefix='/posts')
        app.register_blueprint(check_in_comments_controller, url_prefix='/check_in_comments')
        app.register_blueprint(place_ratings_controller, url_prefix='/place_ratings')
        app.register_blueprint(blacklist_controller, url_prefix='/blacklist')
        app.register_blueprint(search_controller, url_prefix='/search')
        app.register_blueprint(cities_controller, url_prefix='/cities')
        app.register_blueprint(chat_rooms_controller, url_prefix='/chat_rooms')
        app.register_blueprint(chat_room_messages_controller, url_prefix='/chat_room_messages')
        app.register_blueprint(like_controller)
        app.register_blueprint(user_user_activation_controller)

Application Controller
----------------------

The main route of the application is controlled by the ``foodle.controllers.application_controller`` module, which defines the home route like so:

  .. code-block:: python

    @application_controller.route('/', methods=['GET'])
    def index():
        token = request.cookies.get('jwt')

        if token is not None:
            try:
                current_user = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])

                return redirect('/users/' + str(current_user['id']) + '/feed')
            except:
                return redirect('/sessions/new')

        return redirect('/sessions/new')

Database Instantiation and Seeding
**********************************

Database is instantiated with ``init.sql`` file and seeded with ``seed.sql`` file. You may disable seeding option by setting environment variable ``SEED`` to ``false``.

Users API
*********

As it is said before, user is the main entity of the authentication.

  .. code-block:: sql

    --  Create `users` table
    CREATE TABLE users(
        id serial PRIMARY KEY,
        username character varying(255) UNIQUE NOT NULL,
        display_name character varying (255) NOT NULL,
        password_digest character varying(255) NOT NULL,
        activation_key uuid DEFAULT "public".uuid_generate_v4() UNIQUE NOT NULL,
        ip_address inet NOT NULL,
        inserted_at timestamp DEFAULT now() NOT NULL
    );

    --  Create `user_activations` table
    CREATE TABLE user_activations(
        user_id integer PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
        inserted_at timestamp DEFAULT now() NOT NULL
    );

    --  Create `user_images` table
    CREATE TABLE user_images(
        user_id integer PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
        url character varying(255) NOT NULL,
        inserted_at timestamp DEFAULT now() NOT NULL
    );

The ``password_digest`` field holds the hashed value of the users password. ``activation_key`` field holds a ``uuid`` value in order to activate the user and generated by the database routine. ``ip_address`` value holds the IP address of the request sender.

On client-side, the function triggered is:

  .. code-block:: html

    <form id="signup-form">
      <div class="row">
        <div class="large-6 columns show-for-large"><p></p></div>
        <div class="large-4 medium-12 columns">
          <div class="callout main-entity" style="background-color: rgb(230, 230, 230);">
            <h3>Sign Up</h3>
            <div class="row">
              <div class="large-12 columns">
                <label class="username">Username
                  <input type="text" placeholder="7 to 20 characters">
                </label>
              </div>
              <div class="large-12 columns">
                <label class="display-name">Full name
                  <input type="text" placeholder="7 to 20 characters">
                </label>
              </div>
              <div class="large-12 columns">
                <label class="password">Password (minimum 8 characters)
                  <input type="password" placeholder="">
                </label>
              </div>
              <div class="large-12 columns">
                <label class="password-duplicate">Re-enter password
                  <input type="password" placeholder="">
                </label>
              </div>
              <div class="large-12 columns" style="margin-top: 20px;">
                <button type="submit" class="button float-right" style="background-color: green">Sign Up</button>
                <button type="button" class="button float-right" style="margin-right: 10px;" onclick="window.location.href='/';">Go back to homepage</button>
              </div>
            </div>
          </div>
        </div>
        <div class="large-2 columns show-for-large"></div>
      </div>
    </form>

  .. code-block:: javascript

    $('#signup-form').submit(function (event) {
      event.preventDefault();

      const username = $('label.username').children().val();
      const displayName = $('label.display-name').children().val();
      const password = $('label.password').children().val();
      const passwordDuplicate = $('label.password-duplicate').children().val();

      console.log(username, displayName, password, passwordDuplicate);

      if (username.length < 8) {
        alert('Username is shorter than 8 characters.');
      } else if (username.length > 20) {
        alert('Username is longer than 20 characters.');
      } else if (displayName.length < 8) {
        alert('Display name should be longer than 8 characters.');
      } else if (displayName.length > 20) {
        alert('Display name should be shorter than 20 characters.');
      } else if (password.length < 8 || passwordDuplicate.length < 8) {
        alert('Password should be 8 characters long, at least.');
      } else {
        if (password === passwordDuplicate) {
          $.ajax({
            method: 'POST',
            url: '/users/',
            data: JSON.stringify({
              username: username,
              display_name: displayName,
              password: password,
            }),
            contentType: 'application/json'
          })
          .success(function (data, textStatus, xhr) {
            window.location.replace(xhr.getResponseHeader('location'));
          })
          .fail(function (data, textStatus, xhr) {
            alert('User with same name already exists.');
          })
        } else {
          alert('Password and re-enter password fields are not same.');
          //  Set focus to the password field
          $('label.password').children().focus()
        }
      }
    });

A user could be created via ``:create`` action through ``:new`` action.

  .. code-block:: python

    @users_controller.route('/new', methods=['GET'])
    def new():
        return render_template('/users/new.html')

Notice this route does not apply any kind of authentication step.

  .. code-block:: python

    @users_controller.route('/', methods=['POST'])
    def create():
        username = request.json.get('username')
        password = request.json.get('password')
        display_name = request.json.get('display_name')
        ip_address = request.access_route[0]

        if not isinstance(username, str) or not isinstance(password, str) or not isinstance(display_name, str):
            return "Request body is unprocessable.", 422

        username_pattern = re.compile("[a-zA-Z0-9]{3,20}")
        password_pattern = re.compile("[a-zA-Z0-9]{7,20}")

        if not password_pattern.match(password) or not username_pattern.match(username):
            return "Username and password should be alphanumeric and be 5 to 20 characters long.", 422

        password_digest = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(
                """
                INSERT INTO users
                (username, display_name, password_digest, ip_address)
                VALUES (%s, %s, %s, %s)
                RETURNING *
                """,
                [username, display_name, password_digest, ip_address])

                user = curs.fetchone()

                resp = make_response()

                user['inserted_at'] = user['inserted_at'].isoformat()

                token = jwt.encode(user, current_app.secret_key, algorithm='HS256')
                resp.set_cookie('jwt', value=token)
                resp.headers['location'] = '/users/' + str(user['id']) + '/feed'

                return resp, 201

It could be updated via ``:update`` action triggered through ``:edit`` action.

  .. code-block:: python

    @users_controller.route('/<int:id>/edit', methods=['GET'])
    @auth_hook_functor
    def edit(id):
        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                SELECT u.id,
                       u.username,
                       u.display_name,
                       count(uf.id) number_of_friends,
                       ui.url image_url,
                       max(p.inserted_at) last_posted,
                       count(p.id) number_of_posts
                FROM users u
                LEFT OUTER JOIN user_images ui ON ui.user_id = u.id
                LEFT OUTER JOIN user_friends uf ON uf.user_id = u.id
                LEFT OUTER JOIN posts p ON p.user_id = u.id
                GROUP BY u.id, ui.user_id
                HAVING u.id = %s;
                """,
                [id])

                user = curs.fetchone()

                if user is not None:
                    return render_template('/users/edit.html', user=user)
                else:
                    return "Entity not found.", 404



  .. code-block:: python

    @users_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
    @auth_hook_functor
    def update(id):
        username = request.json.get('username')
        password = request.json.get('password')
        user_image_url = request.json.get('user_image_url')

        request.json['id'] = id

        if password is not None:
            if not isinstance(username, str) or not isinstance(password, str):
                return "Request body is unprocessable.", 422

            request.json['password_digest'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            with psycopg2.connect(foodle.app.config['dsn']) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as curs:
                    curs.execute(
                    """
                    BEGIN
                    """
                    )

                    image = None

                    if len(user_image_url) > 0:
                        curs.execute(
                        """
                        UPDATE user_images
                        SET url = %s
                        WHERE user_id = %s
                        RETURNING *
                        """,
                        [user_image_url, id])

                        image = curs.fetchone()

                        if curs.rowcount == 0:
                            curs.execute(
                            """
                            INSERT INTO user_images
                            (user_id, url)
                            VALUES (%s, %s)
                            RETURNING *
                            """,
                            [id, user_image_url])

                            image = curs.fetchone()

                    curs.execute(
                    """
                    UPDATE users
                    SET username = %(username)s,
                        password_digest = %(password_digest)s,
                        display_name = %(display_name)s
                    WHERE id = %(id)s
                    RETURNING *
                    """, request.json)

                    rowCount = curs.rowcount
                    user = curs.fetchone()

                    curs.execute(
                    """
                    COMMIT
                    """
                    )

                    if rowCount is not 0:
                        resp = make_response()
                        user['inserted_at'] = user['inserted_at'].isoformat()
                        user['url'] = image['url']

                        token = jwt.encode(user, current_app.secret_key, algorithm='HS256')
                        resp.set_cookie('jwt', value=token)

                        resp.headers['location'] = '/users/' + str(id)

                        return resp
                    else:
                        return "Entity not found.", 404
        else:
            if not isinstance(username, str):
                return "Request body is unprocessable.", 422

            with psycopg2.connect(foodle.app.config['dsn']) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as curs:
                    curs.execute(
                    """
                    BEGIN
                    """
                    )

                    image = None

                    if len(user_image_url) > 0:
                        curs.execute(
                        """
                        UPDATE user_images
                        SET url = %s
                        WHERE user_id = %s
                        RETURNING url
                        """,
                        [user_image_url, id])

                        image = curs.fetchone()

                        if curs.rowcount == 0:
                            curs.execute(
                            """
                            INSERT INTO user_images
                            (user_id, url)
                            VALUES (%s, %s)
                            RETURNING *
                            """,
                            [id, user_image_url])

                            image = curs.fetchone()

                    curs.execute(
                    """
                    UPDATE users
                    SET username = %(username)s,
                        display_name = %(display_name)s
                    WHERE id = %(id)s
                    RETURNING *
                    """, request.json)

                    rowCount = curs.rowcount
                    user = curs.fetchone()

                    curs.execute(
                    """
                    COMMIT
                    """
                    )

                    if rowCount is not 0:
                        resp = make_response()
                        user['inserted_at'] = user['inserted_at'].isoformat()
                        user['url'] = image['url']

                        token = jwt.encode(user, current_app.secret_key, algorithm='HS256')
                        resp.set_cookie('jwt', value=token)

                        resp.headers['location'] = '/users/' + str(id)

                        return resp
                    else:
                        return "Entity not found.", 404

To reach the profile page of a specific user,

Feed API
********

Feed view aggregates the database through posts, places and users.

  .. code-block:: sql

    CREATE VIEW feed AS
        SELECT u.id user_id,
            u.display_name,
            ui.url user_image,
            po.id post_id,
            po.inserted_at,
            po.title post_title,
            po.body post_body,
            po.cost cost_of_meal,
            po.score post_score,
            pl.name place_name,
            pl.id place_id,
            count(l.user_id) like_count
        FROM posts po
        INNER JOIN places pl ON pl.id = po.place_id
        INNER JOIN users u ON u.id = po.user_id
        LEFT OUTER JOIN user_images ui ON ui.user_id = u.id
        LEFT OUTER JOIN post_likes l ON l.post_id = po.id
        GROUP BY u.id, u.display_name, ui.url, po.id, po.inserted_at, po.title, po.body, po.cost, po.score, pl.name, pl.id, l.post_id
        ORDER BY po.inserted_at DESC, po.id DESC;

It could be accessed through ``GET /users/{id}/feed``

  .. code-block:: python

    @feed_controller.route('/<int:id>/feed/', methods=['GET'])
    @auth_hook_functor
    def index(id):
        if g.current_user['id'] is not id:
            return "Forbidden", 401

        limit = request.args.get('limit') or 20
        offset = request.args.get('offset') or 0

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(
                """
                BEGIN
                """
                )

                curs.execute(
                """
                SELECT url
                FROM user_images
                WHERE user_id = %s
                """,
                [id])

                image_url = None

                try:
                    image_url = curs.fetchone()['url']
                except:
                    pass

                curs.execute(
                """
                SELECT f.*, pl.user_id IS NOT NULL is_liked
                FROM feed f
                LEFT OUTER JOIN post_likes pl ON (f.post_id = pl.post_id AND pl.user_id = %s)
                LIMIT %s
                OFFSET %s
                """,
                [id, limit, offset])

                feeds = curs.fetchall()

                for each_feed in feeds:
                    curs.execute(
                    """
                    SELECT link
                    FROM post_images
                    WHERE post_id = %s
                    LIMIT 5
                    """,
                    [each_feed['post_id']])

                    each_feed['post_images'] = curs.fetchall()

                    curs.execute(
                    """
                    SELECT pc.id, pc.body, pc.inserted_at, ui.url, u.display_name, u.id user_id
                    FROM post_comments pc
                    INNER JOIN users u ON u.id = pc.user_id
                    LEFT OUTER JOIN user_images ui ON ui.user_id = u.id
                    WHERE post_id = %s
                    ORDER BY pc.inserted_at ASC
                    """,
                    [each_feed['post_id']])

                    each_feed['post_comments'] = curs.fetchall()

                curs.execute(
                """
                COMMIT
                """
                )

                return render_template('/users/feed/index.html', feeds=feeds, image_url=image_url, user_id=id)

To activate an existing user, we should call ``:create`` action on ``user_user_activation_controller``:

  .. code-block:: python

    @user_user_activation_controller.route('/users/<int:user_id>/user_activation', methods=['POST'])
    @auth_hook_functor
    def create(user_id):
        if g.current_user['id'] != user_id:
            return "Forbidden.", 401

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute("BEGIN")

                curs.execute(
                """
                SELECT activation_key
                FROM users u
                WHERE u.id = %s
                """,
                [user_id])

                activation_key = curs.fetchone()[0]

                print(request.json.get('activation_key'))
                print(activation_key)

                if request.json.get('activation_key') == activation_key:
                    curs.execute(
                    """
                    INSERT INTO user_activations
                    (user_id)
                    VALUES (%s)
                    """,
                    [user_id])

                    rowCount = curs.rowcount

                    curs.execute("COMMIT")

                    if rowCount is not 0:
                        return "User activated.", 201
                    else:
                        return "Entity not found.", 404
                else:
                    curs.execute("ROLLBACK")

                    return "Wrong activation key.", 405


Posts API
*********

Post entity holds the post data.

  .. code-block:: sql

    -- Create `posts` table
    CREATE TABLE posts(
        id serial PRIMARY KEY,
        title text NOT NULL,
        body text NOT NULL,
        cost integer NOT NULL,
        score integer NOT NULL,
        user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
        place_id integer NOT NULL REFERENCES places(id) ON DELETE CASCADE ON UPDATE CASCADE,
        inserted_at timestamp DEFAULT now() NOT NULL
    );

To create a post entity, we need to trigger ``:create`` action via ``:new`` action.

  .. code-block:: python

    @posts_controller.route('/', methods=['POST'])
    @auth_hook_functor
    def create():
        request.json['user_id'] = g.current_user['id']

        if not isinstance(request.json.get('body'), str):
            return "Request body is unprocessable.", 422

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                INSERT INTO posts
                (title, body, cost, score, user_id, place_id)
                VALUES (%(title)s, %(body)s, %(cost)s, %(score)s, %(user_id)s, %(place_id)s)
                RETURNING *
                """, request.json)

                rowCount = curs.rowcount
                post = curs.fetchone()

                if request.json.get('image-url') is not None:
                    curs.execute(
                    """
                    INSERT INTO post_images
                    (post_id, link, ip_addr)
                    VALUES (%s, %s, %s)
                    """,
                    [post['id'], request.json.get('image-url'), request.access_route[0]])

                if rowCount is not 0:
                    return "Created.", 201
                else:
                    return "Entity not found.", 404

To update an existing post, we would trigger ``:update`` action via ``:edit`` action.

  .. code-block:: python

    @posts_controller.route('/<int:id>/edit', methods=['GET'])
    @auth_hook_functor
    def edit(id):
        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                SELECT p.id post_id,
                       p.body,
                       p.title,
                       p.cost,
                       p.score,
                       p.inserted_at,
                       u.id user_id,
                       u.display_name,
                       u.username,
                       pl.id place_id,
                       pl.name place_name
                FROM posts p
                INNER JOIN users u ON u.id = p.user_id
                INNER JOIN places pl ON pl.id = p.place_id
                WHERE p.id = %s
                """,
                [id])

                post = curs.fetchone()

                if g.current_user['id'] != post['user_id']:
                    return "Whoosh. You sneaky little' thing!", 401

                curs.execute(
                """
                SELECT link
                FROM post_images pi
                WHERE pi.post_id = %s
                """,
                [id])

                post_image_urls = curs.fetchall()

                if post is not None:
                    return render_template('/posts/edit.html', post=post, post_image_urls=post_image_urls)
                else:
                    return "Entity not found.", 404

    @posts_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
    @auth_hook_functor
    def update(id):
        if request.json.get('id') is not None:
            return "Request body is unprocessable.", 422

        request.json['id'] = id

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                BEGIN
                """
                )

                curs.execute(
                """
                UPDATE posts
                SET title = %(title)s,
                    body = %(body)s,
                    cost = %(cost)s,
                    score = %(score)s
                WHERE id = %(id)s
                RETURNING *
                """, request.json)

                if curs.fetchone()['user_id'] != g.current_user['id']:
                    curs.execute(
                    """
                    ROLLBACK
                    """
                    )
                    return "Forbidden.", 201

                curs.execute(
                """
                COMMIT
                """
                )

                if curs.rowcount is not 0:
                    return "Changed.", 201
                else:
                    return "Entity not found.", 404

Also, to delete a post, we would trigger ``:delete`` action.

  .. code-block:: python

    @posts_controller.route('/<int:id>', methods=['DELETE'])
    def delete(id):
        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                DELETE FROM posts
                WHERE id = %s
                """, [id])

                if curs.rowcount is not 0:
                    return "", 204
                else:
                    return "Entity not found.", 404

Search Bar
**********

This feature is implemented by ``search_controller``, which queries database with **LIKE** query and returns relevant results.

  .. code-block:: html

    <input id="search" type="search" placeholder="Search people, places and cities..." style="display: inline;" autocomplete="off" maxlength="20" disabled>

Results will be shown with following callout:

  .. code-block:: html

    <div class="row top-bar-extend-cell cell-0">
      <a>
        <div class="small-2 columns">
          <div class="profile-image-search"></div>
        </div>
        <div class="small-10 columns">
          <p class="display-name"></p></br>
          <p><span class="username"></span></p>
        </div>
      </a>
    </div>

On each key press event, we call the following function:

  .. code-block:: javascript

    var semaphore = 0;  // Used for Ninja JS engine, proprietary WebKit.

    $('#search').on('keydown', function (keyEvent) {
      setTimeout(function () {
        const result = $('#search').val();

        if (result !== '') {
          semaphore += 1;

          $.ajax({
            method: 'GET',
            url: '/search?parameter=' + result
          })
          .success(function (data, textStatus, xhr) {
            semaphore -= 1;

            if (!semaphore) {
              for (var i = 0; i < 5; ++i) {
                $('.cell-' + i).css('border-radius', '0');
                $('.cell-' + i).css('visibility', 'hidden');
              }

              $('#search').css('color', 'black');

              $('.top-bar-extend').css('visibility', 'visible');

              var dataCount = 0;

              $('.cell-0').css('border-radius', '10px 10px 0 0');

              for (var i = 0; i < data[0].length; ++i, ++dataCount) {
                $('.cell-' + dataCount).css('visibility', 'visible');
                $('.cell-' + dataCount + ' p.display-name')[0].innerHTML = data[0][i][2];
                $('.cell-' + dataCount + ' span.username')[0].innerHTML = '@' + data[0][i][1];
                $('.cell-' + dataCount + ' span.username').css('color', 'rgb(170, 170, 170)');
                $('.cell-' + dataCount + ' a').attr('href', '/users/' + data[0][i][0]);
                $('.cell-' + dataCount + ' .profile-image-search').css('background-image', 'url(' + data[0][i][3] + ')');
              }

              for (var i = 0; i < data[1].length; ++i, ++dataCount) {
                $('.cell-' + dataCount).css('visibility', 'visible');
                $('.cell-' + dataCount + ' p.display-name')[0].innerHTML = data[1][i][0];
                $('.cell-' + dataCount + ' span.username')[0].innerHTML = data[1][i][1];
                $('.cell-' + dataCount + ' a').attr('href', '/places/' + data[1][i][3]);
                $('.cell-' + dataCount + ' .profile-image-search').css('background-image', 'url(' + data[1][i][2] + ')');
              }

              if (dataCount === 1) {
                $('.cell-0').css('border-radius', '10px');
              } else if (dataCount === 0) {
                $('#search').css('color', 'red');
              } else {
                $('.cell-' + (dataCount - 1)).css('border-radius', '0 0 10px 10px');
              }
            }
          });
        } else {
          $('.top-bar-extend').css('visibility', 'hidden');
          $('.top-bar-extend-cell').css('visibility', 'hidden');
        }
      }, 5);
    });


Which triggers the following route action in server-side:

  .. code-block:: python

    @search_controller.route('/', methods=['GET'])
    def index():
        parameter = request.args.get('parameter')

        if parameter is not None:
            with psycopg2.connect(foodle.app.config['dsn']) as conn:
                with conn.cursor(cursor_factory=DictCursor) as curs:
                    curs.execute(
                    """
                    SELECT u.id, u.username, u.display_name, ui.url
                    FROM users u
                    LEFT OUTER JOIN user_images ui ON u.id = ui.user_id
                    WHERE u.display_name ILIKE %s OR
                          u.username ILIKE %s ESCAPE '='
                    LIMIT 5
                    """,
                    ['%' + parameter + '%', '%' + parameter + '%'])

                    users = curs.fetchall()

                    if len(users) < 5:
                        remaining = 5 - len(users)

                        curs.execute(
                        """
                        SELECT p.name, p.description, pi.url, p.id
                        FROM places p
                        LEFT OUTER JOIN place_images pi ON p.id = pi.place_id
                        WHERE p.name ILIKE %s OR
                              p.description ILIKE %s ESCAPE '='
                        LIMIT %s
                        """,
                        ['%' + parameter + '%', '%' + parameter + '%', remaining])

                        places = curs.fetchall()

                        return jsonify([users, places])
                    else:
                        return jsonify([users])
        else:
            return "Invalid request.", 422
