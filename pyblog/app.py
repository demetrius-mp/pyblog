import os

from flask import Flask

from pyblog.extensions import configuration


def create_app():
    app = Flask(__name__)

    env_vars = ('SECRET_KEY',)

    for env_var in env_vars:
        if env_var not in app.config:
            app.config[env_var] = os.environ.get(env_var)
    configuration.init_app(app)

    return app
