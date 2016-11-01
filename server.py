#!/usr/bin/env python3
import os
from foodle import app
from foodle.db import init
from foodle.router import bootstrap

if __name__ == "__main__":
    app_port = os.getenv('VCAP_APP_PORT')

    if app_port is not None:
        port, debug = int(app_port), False
    else:
        port, debug = 5000, True

    init()
    bootstrap()

    app.run(host='0.0.0.0', port=port, debug=debug)
