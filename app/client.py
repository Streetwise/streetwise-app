""" Client App """

import os
from flask import Blueprint, render_template

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
    return send_file(path.join(Config.DIST_DIR, 'favicon.ico'))

@client_bp.route('/loading.gif')
def index_loading():
    return send_file(path.join(Config.DIST_DIR, 'loading.gif'))
