"""
Security Functions
https://github.com/auth0/auth0-python
"""

from functools import wraps
from flask import request
from flask_restplus import abort

from .. import Config

def require_auth(func):
    """ Secure method decorator """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verify if User is Authenticated
        # Authentication logic goes here
        if request.headers.get('authorization') == Config.API_KEY:
            return func(*args, **kwargs)
        else:
            return abort(401)
    return wrapper
