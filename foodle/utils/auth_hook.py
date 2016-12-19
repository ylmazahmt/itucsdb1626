from functools import wraps
from flask import request, current_app, g, redirect
import jwt

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
