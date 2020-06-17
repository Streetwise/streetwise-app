"""
Global Flask Application Setting
See `.flaskenv` for default settings.
 """

import os, os.path

APP_DIR = os.path.dirname(__file__)

# ../data/streetwise.db
DATA_PATH = os.path.abspath(os.path.join(APP_DIR, os.pardir, 'data', 'streetwise.db'))

DEFAULT_BUCKET_URL = "https://imagery.streetwise-app.ch/campaigns"

class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    FLASK_SECRET = os.getenv('FLASK_SECRET', 'NoSecret')
    # Set API_KEY on your production Environment
    API_KEY = os.getenv('API_KEY', 'OpenData')

    SSL_REDIRECT = os.getenv('SSL_REDIRECT', False)

    IMAGE_BUCKET_URL = os.getenv('IMAGE_BUCKET_URL', DEFAULT_BUCKET_URL)

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + DATA_PATH)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, 'dist')

    # Check for frontend build
    if not os.path.exists(DIST_DIR):
        raise Exception(
            'DIST_DIR not found: {}'.format(DIST_DIR))
