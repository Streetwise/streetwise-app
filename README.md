# Streetwise App

Mobile web application for the Streetwise project. For background information, please visit https://streetwise.space

## History

- **0.1.1** 6.5.2020: Patch release
- **0.1.0** 29.4.2020: Initial release

# Developer notes

![Vue Logo](/docs/vue-logo.png "Vue Logo") ![Flask Logo](/docs/flask-logo.png "Flask Logo")

This project uses Flask & Flask-RestPlus to create a REST-style API, accessed through Vue.js to handle the frontend and asset pipeline. Data from the Python server to the Vue application is passed by making Ajax requests.

The API is served using a Flask blueprint at `/api/` using Flask RestPlus class-based resource routing.

A Flask view is used to serve the `index.html` as an entry point into the Vue app at the endpoint `/`.

Additional endpoints currently include: `/tour` `/wise` `/complete`

### Components

* [Flask](https://flask.palletsprojects.com/), a [Python](https://python.org) web framework
* [Flask-RestPlus](https://flask-restplus.readthedocs.io/en/stable/) API layer
* [SQLAlchemy](https://docs.sqlalchemy.org/) data persistence
* [PyTest](https://pytest.org) test suite
* [Vue.js v2](https://vuejs.org/v2/guide/) front-end framework
* [vue-cli](https://github.com/vuejs/vue-cli/blob/dev/docs/README.md), [Vuex](https://vuex.vuejs.org/), [Router](https://router.vuejs.org/)
* [Axios](https://github.com/axios/axios/) for backend communication with [Vue Filters](https://vuejs.org/v2/guide/filters.html)
* Gunicorn web server support
* Heroku deployment support

### Project structure

The template uses vue-cli 3 and assumes Vue Cli & Webpack will manage front-end resources and assets, so it does overwrite template delimiter.

The Vue instance is preconfigured with Filters, Vue-Router, Vuex; each of these can easilly removed if they are not desired.

| Location             |  Content                                   |
|----------------------|--------------------------------------------|
| `/app`               | Flask Application                          |
| `/app/api`           | Flask Rest Api (`/api`)                    |
| `/app/client.py`     | Flask Client (`/`)                         |
| `/src`               | Vue App .                                  |
| `/src/main.js`       | JS Application Entry Point                 |
| `/public/index.html` | Html Application Entry Point (`/`)         |
| `/public/static`     | Static Assets                              |
| `/dist/`             | Bundled Assets Output (generated at `yarn build` |

## Installation

First, clone this repository and make sure to set up the following dependencies:

- [X] Python 3
- [X] Python Poetry - [instructions](https://python-poetry.org/docs/)
- [X] Yarn - [instructions](https://yarnpkg.com/en/docs/install)
- [X] Vue cli 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
- [X] Heroku cli (if deploying to Heroku)

Setup a virtual environment, install dependencies, and activate it:

```
$ poetry install
$ poetry shell
```

Create a file called `.flaskenv` in the root folder and add development settings:

```
# Production Enviroment should be set to 'production'
FLASK_ENV = "development"
FLASK_APP = "app"

# Uncomment this to debug:
FLASK_DEBUG = 1
```

### Initial data import

Import the image files, which should be in the `ch_data.csv` file in the `data` folder:

`python import.sh`

This will also create a blank database.

### Frontend setup

Install JS dependencies

```
$ yarn
```

Run the test suite to make sure we're up to scratch (do it at this point, since it will expect frontend set up to be complete):

```
$ pytest
```

Start the Webpack dev server:

```
$ yarn serve
```

Start the development server (in a separate tab from Webpack):

```
$ python run.py
```

### Notes

The Vue application will be served from http://localhost:8080
The API and static files will be served from http://localhost:5000

The dual dev-server setup allows you to take advantage of Webpack's development server with hot module replacement.

Proxy config in `vue.config.js` is used to route the requests back to Flask's API on port 5000.

If you would rather run a single dev server, you can run Flask's development server only on `:5000`, but you have to build build the Vue app first, and the page will not reload on changes:

```
$ yarn build
$ python run.py
```

## Production

For a good introduction to production Flask apps, see [freecodecamp article by Greg Obinna](https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/).

This template is configured to work with Heroku + Gunicorn and is pre-configured to have Heroku build the application before releasing it.

Heroku's nodejs buildpack will handle install for all the dependencies from the `packages.json` file.
It will then trigger the `postinstall` command which calls `yarn build`.
This will create the bundled `dist` folder which will be served by whitenoise.

Heroku's buildpack currently does not Python dependencies from poetry automatically. [We're working on it](https://github.com/heroku/heroku-buildpack-python/issues/796#issuecomment-611198469) ...

#### Sever Setup

To deploy using the Web wizard:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/streetwise/streetwise-app)

To get things set up on the Heroku side using the CLI:

```
$ heroku apps:create flask-vuejs-template-demo
$ heroku git:remote --app flask-vuejs-template-demo
$ heroku buildpacks:add --index 1 heroku/nodejs
$ heroku buildpacks:add --index 2 heroku/python
$ heroku config:set FLASK_ENV=production
$ heroku config:set FLASK_SECRET=SuperSecretKey

$ git push heroku
```

## Acknowledgements

This project was started with parts of [smartuse/platform](https://github.com/smartuse/platform) and [gtalarico/flask-vuejs-template](https://github.com/gtalarico/flask-vuejs-template).
