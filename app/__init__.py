from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path

# TODO: track solution to https://github.com/jarus/flask-testing/issues/143
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

db = SQLAlchemy()
migrate = Migrate()

from .config import Config

def create_app():
    app = Flask(__name__, static_folder='../dist/static')
    app.config.from_object('app.config.Config')
    app.logger.info('>>> {}'.format(Config.FLASK_ENV))

    db.init_app(app)
    from app.models import Base, Image, Session, Comment, Vote
    migrate.init_app(app, db)

    # Initialize the API limiter
    from .api import api_limiter
    api_limiter.init_app(app)

    # Register the API blueprint
    from .api import api_bp
    app.register_blueprint(api_bp)

    from .client import client_bp
    # TODO: enable if we need additional client logic
    # app.register_blueprint(client_bp)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    return app
