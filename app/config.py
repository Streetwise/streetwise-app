"""
Global Flask Application Setting
See `.flaskenv` for default settings.
 """

import os, os.path

DEFAULT_BUCKET_URL = "https://eu-central-1.linodeobjects.com/streetwise/enhanced/"

# ../data/streetwise.db
DEFAULT_DB_PATH = os.path.dirname(__file__)
DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_PATH, os.pardir, 'data', 'streetwise.db')
DEFAULT_DB_PATH = os.path.abspath(DEFAULT_DB_PATH)


class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    SSL_REDIRECT = os.getenv('SSL_REDIRECT', False)

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + DEFAULT_DB_PATH)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    IMAGE_BUCKET_URL = os.getenv('IMAGE_BUCKET_URL', DEFAULT_BUCKET_URL)

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, 'dist')

    if not os.path.exists(DIST_DIR):
        raise Exception(
            'DIST_DIR not found: {}'.format(DIST_DIR))
