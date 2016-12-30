Parts Implemented by Muratcan Şahin
===================================
This document contains information to guide developer for the features that I implemented.
This document contains flask codes, sql statements for creating, editing and deleting data which stored in database, Javascript codes that used for front-end development and database design.
1. `Flask`_
  a.`Used Libraries`_
2.`Front-End Development`_
  a.`JavaScript Codes`_
  b.`HTML Codes`_
3.`Database Design`_
  a.`Post Like Table`_
  b.`Post Comments Table`_
  c.`Post Images Table`_

Flask
**************

Used Libraries
--------------
**Used libraries for flask application**

  .. code-block:: python

    import foodle
    import psycopg2
    from flask import Blueprint, render_template, current_app, request, jsonify, redirect, make_response, g
    from psycopg2.extras import RealDictCursor, DictCursor
    from foodle.utils.auth_hook import auth_hook_functor

Front-End Development
*********************

JavaScript Codes
----------------
Post Like
++++++++++
**We assign an on-click event handler to each like button**
  .. code-block:: javascript
    $.each($('.like-button'), function (i, element) {
      if ($(this).attr('data-exists') === 'True') {
        $(this).addClass('enabled');
      }

      $(element).click(function () {
        var self = this;

        if ($(self).attr('data-exists') === 'False') {
          $.ajax({
            method: 'POST',
            url: $(self).attr('data-ajax'),
            data: JSON.stringify({
              user_id: $('#container').attr('data-sender-id')
            }),
            contentType: 'application/json'
          })
          .success(function () {
            var split = $(self)[0].innerHTML.split(' ');
            var count = parseInt(split[5]);
            count += 1;
            split[5] = '' + count;
            $(self)[0].innerHTML = split.join(' ');

            $(self).addClass('enabled');
            $(self).attr('data-exists', 'True');
          });
        } else {
          $.ajax({
            method: 'DELETE',
            url: $(self).attr('data-ajax'),
            data: JSON.stringify({
              user_id: $('#container').attr('data-sender-id')
            }),
            contentType: 'application/json'
          })
          .success(function () {
            var split = $(self)[0].innerHTML.split(' ');
            var count = parseInt(split[5]);
            count -= 1;
            split[5] = '' + count;
            $(self)[0].innerHTML = split.join(' ');

            $(self).removeClass('enabled');
            $(self).attr('data-exists', 'False');
          });
        }
      });
    });


HTML Codes
-----------
Post Like
+++++++++++
**Like button implementation to feed**
  .. code-block:: html
    <div class="large-6 columns"><a class="button float-center social-button like-button" data-ajax="/posts/{{ each_feed.post_id }}/like" data-exists="{{ each_feed.is_liked }}"><i class="fa fa-thumbs-up" aria-hidden="true"></i>  {{ each_feed.like_count }} like</a></div>





Post Comment
++++++++++++
**Post comment implementation of all comments in callout**
  .. code-block:: html
    {% if each_feed.post_comments|length == 0 %}
    <div class="large-6 columns"><a class="button float-center social-button"><i class="fa fa-pencil" aria-hidden="true"></i>  No comment</a></div>
    {% elif each_feed.post_comments|length == 1 %}
    <div class="large-6 columns"><a class="button float-center social-button"><i class="fa fa-pencil" aria-hidden="true"></i>  {{ each_feed.post_comments|length  }} comment</a></div>
    {% else %}
    <div class="large-6 columns"><a class="button float-center social-button"><i class="fa fa-pencil" aria-hidden="true"></i>  {{ each_feed.post_comments|length  }} comments</a></div>
    {% endif %}
    </div>
    <hr>
    <div class="row" style="margin-left: 0; margin-right: 0; margin-top: 10px;">
    {% for each_post_comment in each_feed.post_comments %}
    <div class="row" style="margin-left: 0; margin-right: 0;">
      <div class="large-1 columns" style="background-image: url('{{ each_post_comment.url }}'); background-size: cover; background-position: center; height: 50px; border-radius: 3px;"></div>
      <div class="large-11 columns">
        <p style="display: inline; font-weight: 500; margin-right: 5px;"><a href="/users/{{each_post_comment.user_id}}">{{ each_post_comment.display_name }}</a></p>
        <p style="display: inline; font-size: 8pt;" class="timestamp">{{ each_post_comment.inserted_at }}</p>
        {% if g.current_user['id'] == each_post_comment.user_id %}
        <button style="display: inline;" onClick="deleteComment({{ each_feed.post_id }}, {{ each_post_comment.id }})">&nbsp;<i class="fa fa-trash-o" style="color: lightGrey; font-size: 10pt;" aria-hidden="true"></i></button>
        {% endif %}
        <br>
        <p>{{ each_post_comment.body }}</p>
      </div>
    </div>

    {% endfor %}

**Post comment implementation of text box**
  .. code-block:: html
    <div class="row" style="margin-left: 0; margin-right: 0;">
      <div class="large-1 columns" style="background-image: url('{{ image_url }}'); background-size: cover; background-position: center; height: 50px; border-radius: 3px;"></div>
      <div class="large-11 columns">
        <form id="post-comment-{{ each_feed.post_id }}" action="">
          <textarea id="post-comment-textarea-{{ each_feed.post_id }}" class="post-comment-textarea" style="display: block; width: 100%; font-size: 10pt; border-radius: 3px; border: 1px solid lightGrey; padding: 5px;" placeholder="Leave a comment..." data-ajax="/posts/{{ each_feed.post_id }}/comments/"></textarea>
        </form>
      </div>
    </div>



Post Image
+++++++++++++
**Post image implementation to posts**
{% for each_feed_image in each_feed.post_images %}
<img class="post-image" src="{{ each_feed_image.link }}" />
{% endfor %}


Databese Design
***************

Post Like Table
---------------
* 'post_likes table stores the data of likes of each post, the user that liked it and inserted time.

                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | post_id       | INTEGER    |   1       |  1        |
                +---------------+------------+-----------+-----------+
                |user_id        | INTEGER    |   1       |  1        |
                +---------------+------------+-----------+-----------+
                |inserted_at    | TIMESTAMP  |   1       |  0        |
                +---------------+------------+-----------+-----------+

'post_id' is a foreign key which references from id entity of 'posts' table.

'user_id' is a foreign key which references from id entity of 'users' table.

Creating Table
++++++++++++++

  .. code-block:: sql

    CREATE TABLE post_likes(
        post_id integer NOT NULL REFERENCES posts(id) ON DELETE CASCADE ON UPDATE CASCADE,
        user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
        inserted_at timestamp DEFAULT now() NOT NULL,
        PRIMARY KEY (post_id, user_id)
    );


**In order to get likes of a post**
  .. code-block:: sql

    @like_controller.route('/posts/<int:post_id>/like', methods=['GET'])
    @auth_hook_functor
    def show(post_id):

        user_id = g.current_user['id']

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(
                """
                SELECT u.id, p.id, pl.*
                FROM post_likes pl
                RIGHT OUTER JOIN users u ON u.id = pl.user_id
                RIGHT OUTER JOIN posts p ON p.id = pl.post_id
                WHERE u.id = %s AND
                      p.id = %s
                """,
                [user_id, post_id])

                like = curs.fetchone()

                if not like is None:
                    return jsonify(like)
                else:
                    return "Like not found", 404

**In order to like a post**
  .. code-block:: sql

    @like_controller.route('/posts/<int:post_id>/like', methods=['POST'])
    @auth_hook_functor
    def create(post_id):
        user_id = g.current_user['id']

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(
                """
                INSERT INTO post_likes
                (post_id, user_id)
                VALUES (%s, %s)
                RETURNING *
                """,
                [post_id, user_id])

                like = curs.fetchone()
                if not like is None:
                    return jsonify(like)
                else:
                    return 404

**In order to dislike a post**
  .. code-block:: sql

    @like_controller.route('/posts/<int:post_id>/like', methods=['DELETE'])
    @auth_hook_functor
    def delete(post_id):
        user_id = g.current_user['id']

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(
                """
                DELETE FROM post_likes
                WHERE post_id = %s AND
                      user_id = %s
                """,
                [post_id, user_id])

                if curs.rowcount is 1:
                    return "", 204
                else:
                    return "Like not found.", 404

Post Comments Table
-------------------
* 'post_comment' table stores the data of comments with related user and its related post.

                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | id            | INTEGER    |   1       |  1        |
                +---------------+------------+-----------+-----------+
                |user_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |post_id        | INTEGER    |   1       |  0        |
                +---------------+------------+-----------+-----------+
                |body           | TEXT       |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |inserted_at    | TIMESTAMP  |   1       |  0        |
                +---------------+------------+-----------+-----------+


'user_id' is a foreign key which references from id entity of 'users' table.

'post_id' is a foreign key which references from id entity of 'posts' table.

'body' is text type data that holds comment.

'inserted_at' timestamp stores the data of insertion of tuple.

**In order to get all post comments**
  .. code-block:: sql

    @post_comments_controller.route('/', methods=['GET'])
    def index():
        limit = request.args.get('limit') or 20
        offset = request.args.get('offset') or 0

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                SELECT pc.id, u.username, pc.post_id, pc.body
                FROM post_comments AS pc
                INNER JOIN users AS u ON pc.user_id = u.id
                LIMIT %s
                OFFSET %s
                """,
                [limit, offset])

                post_comments = curs.fetchall()

                curs.execute(
                """
                SELECT count(id)
                FROM post_comments
                """)

                count = curs.fetchone()[0]

                return render_template('/post_comments/index.html', post_comments=post_comments, count=count)

**In order to get a single post comment**
  .. code-block:: sql

    @post_comments_controller.route('/<int:id>', methods=['GET'])
    def show(id):
        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                SELECT *
                FROM post_comments
                WHERE id = %s
                """,
                [id])

                post_comment = curs.fetchone()

                if post_comment is not None:
                    return render_template('/post_comments/show.html', post_comment=post_comment)
                else:
                    return "Entity not found.", 404

**In order to insert a comment**
  .. code-block::sql

    @post_comments_controller.route('/<int:post_id>/comments/', methods=['POST'])
    @auth_hook_functor
    def create(post_id):
        user_id = g.current_user['id']
        body = request.json['body']

        if not isinstance(body, str) or not isinstance(user_id, int):
            return "Request body is unprocessable", 422

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                INSERT INTO post_comments
                (user_id, post_id, body)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                [user_id, post_id, body])

                post_comment = curs.fetchone()

                resp = make_response()
                resp.headers['location'] = '/post_comments/' + str(post_comment['id'])

                return resp, 201

**In order to update a comment**
  .. code-block::sql

    @post_comments_controller.route('/<int:id>', methods=['PUT', 'PATCH'])
    def update(id):
        if request.json.get('id') is not None or not isinstance(request.json.get('body'), str):
            return "Request is unprocessable.", 422

        request.json['id'] = id

        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                UPDATE post_comments
                SET body = %(body)s
                WHERE id = %(id)s
                """, request.json)

                if curs.rowcount is not 0:
                    resp = make_response()
                    resp.headers['location'] = '/post_comments/' + str(id)

                    return resp, 200
                else:
                    return "Entity not found.", 404

**In order to delete a comment**
  .. code-block::sql
    @post_comments_controller.route('/<int:post_id>/comments/<int:id>/', methods=['DELETE'])
    def delete(post_id, id):
        with psycopg2.connect(foodle.app.config['dsn']) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(
                """
                DELETE FROM post_comments
                WHERE id = %s
                """,
                [id])

                if curs.rowcount is not 0:
                    return "", 204
                else:
                    return "Entity not found.", 404

Post Image Table
----------------
*'post_images' table stores the data of url that is the link of the image with related post.

+---------------+------------+-----------+-----------+
| Name          | Type       | Not Null  |Primary K. |
+===============+============+===========+===========+
| id            | INTEGER    |   1       |  1        |
+---------------+------------+-----------+-----------+
|post_id        | INTEGER    |   1       |  0        |
+---------------+------------+-----------+-----------+
|link           | TEXT       |   1       |  0        |
+---------------+------------+-----------+-----------+
|ip_addr        | INET       |   1       |  0        |
+---------------+------------+-----------+-----------+
|inserted_at    | TIMESTAMP  |   1       |  0        |
+---------------+------------+-----------+-----------+

'post_id' is a foreign key which references from id entity of 'posts' table.

'link' is text type data that holds url of a photo.

'ip_addr' is inet type data that holds the ip of user that send the url.

'inserted_at' timestamp stores the data of insertion of tuple.

**In order to get the post image**
  .. code-block::sql
    curs.execute(
          """
          SELECT link
          FROM post_images pi
          WHERE pi.post_id = %s
          """,
          [id])

          post_image_urls = curs.fetchall()


**In order to insert the post image**
  .. code-block::sql
    curs.execute(
            """
            INSERT INTO post_images
            (post_id, link, ip_addr)
            VALUES (%s, %s, %s)
            """,
            [post['id'], request.json.get('image-url'), request.access_route[0]])

**In order to delete the post image**
In order to delete post image post must be deleted. If post is deleted post image cascades.
