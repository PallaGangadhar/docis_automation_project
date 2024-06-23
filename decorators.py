from functools import wraps
from flask import session, redirect,render_template,request, url_for
from db import *
import requests


def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("loggedin"):
            return f(*args, **kwargs)
        else:
            return redirect("/login")
    return decorated_func

def devices_details_render(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        return func(*args, **kwargs) 
    return decorated_func
