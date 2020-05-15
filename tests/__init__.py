import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from streetwise import create_app, db

app = create_app()
app_context = app.app_context()

if "postgres://" in app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError('Postgres database connection used in testing')
