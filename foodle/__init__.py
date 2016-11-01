#!/usr/bin/env python3
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
