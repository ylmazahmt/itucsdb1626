from functools import wraps
from flask import request, current_app, g
import jwt

def auth_hook_functor(fn):
    @wraps(fn)
    def decorated_fn(*args, **kwargs):
        token = request.cookies.get('jwt')

        if token is None:
            return "You need a token to access that path on web service.", 401
        else:
            g.current_user = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])

            return fn(*args, **kwargs)
    return decorated_fn
