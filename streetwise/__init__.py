from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# TODO: track solution to https://github.com/jarus/flask-testing/issues/143
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

db = SQLAlchemy()
migrate = Migrate()

from .config import Config

def create_app():
    app = Flask(__name__, static_folder='../dist/static')
    app.config.from_object('streetwise.config.Config')
    app.logger.debug('>>> {}'.format(Config.FLASK_ENV))

    if "postgres://" in app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError('Connecting to Postgres database')

    db.init_app(app)
    from .models import Base, Image, Session, Vote, Campaign
    migrate.init_app(app, db)

    # Initialize the API limiter
    from .api import api_limiter
    api_limiter.init_app(app)

    # Register the API blueprint
    from .api import api_bp
    app.register_blueprint(api_bp)

    from .client import client_bp
    app.register_blueprint(client_bp)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    return app
