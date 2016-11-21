#!/usr/bin/env python3

from foodle import app
from foodle.controllers import *

def bootstrap():
    app.register_blueprint(application_controller)
    app.register_blueprint(users_controller, url_prefix='/users')
    app.register_blueprint(user_user_activation_controller, url_prefix='/users')
    # app.register_blueprint(session_controller, url_prefix='/sessions')
    app.register_blueprint(feed_controller, url_prefix='/users')
    app.register_blueprint(user_friends_controller, url_prefix='/users')
    app.register_blueprint(user_friend_requests_controller, url_prefix='/users')
    app.register_blueprint(places_controller, url_prefix='/places')
    app.register_blueprint(place_instances_controller, url_prefix='/place_instances')
    app.register_blueprint(posts_controller, url_prefix='/posts')
    app.register_blueprint(check_ins_controller, url_prefix='/check_ins')
    app.register_blueprint(database_initialization_controller, url_prefix='/database_initialization')
    app.register_blueprint(post_images_controller, url_prefix='/post_images')
    app.register_blueprint(post_comments_controller, url_prefix='/post_comments')
    app.register_blueprint(blacklist_controller, url_prefix='/blacklist')
