#!/usr/bin/env python3
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

import sys
import click

from streetwise import create_app, db
from streetwise.models import *

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,
        Image=Image, Session=Session, Vote=Vote, Campaign=Campaign)


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))
    if os.environ.get('FLASK_ENV') != 'test':
        import subprocess
        # ../data/test.db
        APP_DIR = os.path.dirname(__file__)
        TEST_PATH = os.path.abspath(os.path.join(APP_DIR, 'data', 'test.db'))
        os.environ['FLASK_ENV'] = 'test'
        os.environ['DATABASE_URL'] = 'sqlite:///' + TEST_PATH
        # clear before each run
        try:
            os.remove(TEST_PATH)
        except FileNotFoundError:
            pass
        sys.exit(subprocess.call(sys.argv))

    from flask_migrate import upgrade
    upgrade()
    import pytest
    errno = pytest.main(['tests'])

    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

    sys.exit(errno)

@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()

@app.cli.command()
def init():
    """Run initial deployment tasks."""
    from flask_migrate import init, migrate, upgrade
    # determine the appropriate migration folder
    migration_path = os.environ.get('MIGRATION_PATH')
    if not migration_path: migration_path = 'migrations'
    print('Upgrading from', migration_path)
    init(migration_path)
    migrate(migration_path)
    upgrade(migration_path)

@app.cli.command()
def migrate():
    """Run database migration task."""
    from flask_migrate import migrate
    migration_path = os.environ.get('MIGRATION_PATH')
    if not migration_path: migration_path = 'migrations'
    print('Migrating from', migration_path)
    migrate(migration_path)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    # determine the appropriate migration folder
    migration_path = os.environ.get('MIGRATION_PATH')
    if not migration_path:
        print('MIGRATION_PATH not provided, not upgrading')
    else:
        # migrate database to latest revision
        upgrade(migration_path)
    # Generate some bytes to create entropy
    os.urandom(256)

@app.cli.command()
@click.option('--campaign',
              help='Default name of the campaign (safety, atmos, ..) to use for import.')
@click.option('--src',
              help='Filename of the CSV database to import, e.g. data/test.csv')
@click.option('--update/--no-update', default=True,
              help='Check to see if images are already in database.')
def images(campaign, src, update):
    """Import the images."""
    from streetwise.admin import load_images
    with app.app_context():
        load_images(update, src, campaign)

@app.cli.command()
def profile():
    """ Run profiler and debugger."""
    from flask_debugtoolbar import DebugToolbarExtension
    import flask_profiler

    app.config["flask_profiler"] = {
        "enabled": app.config["DEBUG"],
        "storage": {"engine": "sqlite"},
        "basicAuth": {"enabled": False},
        "ignore": ["^/tests/.*", "^/src"],
    }
    flask_profiler.init_app(app)
    app.config["DEBUG_TB_PROFILER_ENABLED"] = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)
    print(" * Flask profiling running at http://127.0.0.1:4000/flask-profiler/")

if __name__ == '__main__':
    app.cli()
