""" API Blueprint """

from flask import Blueprint, current_app

from flask_restplus import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .. import db

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
api_rest = Api(api_bp)
api_limiter = Limiter(current_app, key_func=get_remote_address)

@api_bp.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


# Import resources to ensure view is registered
# from .resources import * # NOQA
from .images import * # NOQA
from .votes import * # NOQA
