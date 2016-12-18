#!/usr/bin/env python3
import foodle
from flask import Blueprint, render_template, current_app, request, g
from flask_login import login_required
import psycopg2
from psycopg2.extras import RealDictCursor, DictCursor
from foodle.utils.auth_hook import auth_hook_functor

feed_controller = Blueprint('feed_controller', __name__)

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
                SELECT pc.body, pc.inserted_at, ui.url, u.display_name
                FROM post_comments pc
                INNER JOIN users u ON u.id = pc.user_id
                INNER JOIN user_images ui ON ui.user_id = u.id
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
