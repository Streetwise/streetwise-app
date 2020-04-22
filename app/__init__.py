import os
from flask import Flask, current_app, send_file

# TODO: track solution to https://github.com/jarus/flask-testing/issues/143
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from .api import api_bp
from .client import client_bp

app = Flask(__name__, static_folder='../dist/static')

# Register the API blueprint
app.register_blueprint(api_bp)

# TODO: enable if we need additional client logic
# app.register_blueprint(client_bp)

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)

@app.route('/favicon.ico')
def index_favicon():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'favicon.ico')
    return send_file(entry)
