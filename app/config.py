"""
Global Flask Application Setting
See `.flaskenv` for default settings.
 """

import os, os.path
from app import app

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'streetwise.db'))


class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + DB_PATH)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, 'dist')

    if not os.path.exists(DIST_DIR):
        raise Exception(
            'DIST_DIR not found: {}'.format(DIST_DIR))

app.config.from_object('app.config.Config')
