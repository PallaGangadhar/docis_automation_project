from functools import wraps
from flask import session, redirect

def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("loggedin"):
            return f(*args, **kwargs)
        else:
            return redirect("/login")
    return decorated_func
