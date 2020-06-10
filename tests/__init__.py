import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

import os
from flask_migrate import upgrade
from streetwise import create_app, db

app = create_app()
app_context = app.app_context()
upgrade()
