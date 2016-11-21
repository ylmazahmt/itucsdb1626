#!/usr/bin/env python3
import foodle
from flask import Blueprint, render_template, current_app, request
import psycopg2
from psycopg2.extras import RealDictCursor, DictCursor

feed_controller = Blueprint('feed_controller', __name__)

@feed_controller.route('/<int:id>/feed/', methods=['GET'])
def index(id):
    limit = request.args.get('limit') or 20
    offset = request.args.get('offset') or 0

    with psycopg2.connect(foodle.app.config['dsn']) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
            """
            SELECT *
            FROM feed
            LIMIT %s
            OFFSET %s
            """,
            [limit, offset])

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

            return render_template('/users/feed/index.html', feeds=feeds)
