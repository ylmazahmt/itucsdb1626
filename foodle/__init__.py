import datetime
import os
import json
import re
import psycopg2
from flask import Flask

from foodle.controllers import *

def get_elephantsql_dsn(services_env):
    """
    Returns the data source name for ElephantSQL.
    """

    parsed = json.loads(services_env)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)

    return dsn

app = Flask(__name__)

if os.getenv('VCAP_SERVICES') is not None:
    app.config['dsn'] = get_elephantsql_dsn(os.getenv('VCAP_SERVICES'))
else:
    app.config['dsn'] = """host='localhost' port='5432' dbname='foodle_dev' user='main' password='kuz60TOL12'"""

app.register_blueprint(application_controller)
app.register_blueprint(users_controller, url_prefix='/users')
app.register_blueprint(user_user_activation_controller, url_prefix='/users')
# app.register_blueprint(session_controller, url_prefix='/sessions')
# app.register_blueprint(feed_controller, url_prefix='/users')
# app.register_blueprint(user_friends_controller, url_prefix='/users')
app.register_blueprint(places_controller, url_prefix='/places')
# app.register_blueprint(posts_controller, url_prefix='/posts')
# app.register_blueprint(check_ins_controller, url_prefix='/check_ins')
# app.register_blueprint(database_initialization_controller, url_prefix='/database_initialization')
