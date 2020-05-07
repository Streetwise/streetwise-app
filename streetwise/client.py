""" Client App """

from flask import Blueprint, render_template, send_file, send_from_directory
from os import path
from . import Config

client_bp = Blueprint('client_app', __name__,
                      url_prefix='',
                      static_url_path='',
                      static_folder='./dist/static/',
                      template_folder='./dist/',
                      )


@client_bp.route('/')
def index_client():
    return send_file(path.join(Config.DIST_DIR, 'index.html'))

@client_bp.route('/favicon.ico')
def index_favicon():
    return send_file(path.join(Config.DIST_DIR, 'images', 'favicon.ico'))

@client_bp.route('/images/<path:path>')
def index_images(path):
    return send_from_directory(path.join(Config.DIST_DIR, 'images', path))
