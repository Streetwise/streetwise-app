import os
from flask import Flask, current_app, send_file

# TODO: track solution to https://github.com/jarus/flask-testing/issues/143
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

app = Flask(__name__, static_folder='../dist/static')
from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

# Initialize the database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)

from .api import api_bp, api_limiter
from .client import client_bp

# Initialize the API limiter
api_limiter.init_app(app)

# Register the API blueprint
app.register_blueprint(api_bp)

# TODO: enable if we need additional client logic
# app.register_blueprint(client_bp)


@app.route('/')
def index_client():
    return send_file(os.path.join(Config.DIST_DIR, 'index.html'))

@app.route('/favicon.ico')
def index_favicon():
    return send_file(os.path.join(Config.DIST_DIR, 'favicon.ico'))

@app.route('/loading.gif')
def index_loading():
    return send_file(os.path.join(Config.DIST_DIR, 'loading.gif'))
