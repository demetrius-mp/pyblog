import os
import random
import string

from flask import Flask

from pyblog.extensions import configuration


def create_app():
    app = Flask(__name__)

    env_vars = ('SECRET_KEY',)

    for env_var in env_vars:
        if env_var not in app.config:
            random_secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
            app.config[env_var] = os.environ.get(env_var, random_secret_key)
    configuration.init_app(app)

    return app
