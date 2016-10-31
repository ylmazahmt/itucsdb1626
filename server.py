import datetime
import os
import json
import re
import psycopg2 as dbapi2
from flask import Flask
from flask import render_template

from middleware import db
from middleware import bootstrapper

from models import *

app = Flask(__name__)

def get_elephantsql_dsn(services_env):
    # Returns the data source name for ElephantSQL.

    parsed = json.loads(services_env)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)

    return dsn

if __name__ == '__main__':
    app_port = os.getenv('VCAP_APP_PORT')

    if app_port is not None:
        port, debug = int(app_port), False
    else:
        port, debug = 5000, True

    services_env = os.getenv('VCAP_SERVICES')

    if services_env is not None:
        app.config['dsn'] = get_elephantsql_dsn(services_env)
    else:
        app.config['dsn'] = """host='localhost' port='5432' dbname='foodle_dev' user='mask' password='qwerty'"""

    db.__init__(app.config['dsn'])
    bootstrapper.__init__()

    from controllers import *

    app.register_blueprint(application_controller)
    app.register_blueprint(users_controller, url_prefix='/users')
    app.register_blueprint(session_controller, url_prefix='/sessions')
    app.register_blueprint(feed_controller, url_prefix='/users')
    app.register_blueprint(user_friends_controller, url_prefix='/users')
    app.register_blueprint(places_controller, url_prefix='/places')
    app.register_blueprint(posts_controller, url_prefix='/posts')
    app.register_blueprint(check_ins_controller, url_prefix='/check_ins')
    app.register_blueprint(database_initialization_controller, url_prefix='/database_initialization')

    user = User("kerem", "123456", "erke@itu.edu.tr")
    user.hash_password()
    user.save()

    place = Place("Burger King", "The best burger place in town.", user.id)
    place.save()

    post = Post("sdagfdsgfdsfs", user.id)
    post.save()

    check_in = CheckIn(user.id, place.id)
    check_in.save()

    app.run(host='0.0.0.0', port=port, debug=debug)
