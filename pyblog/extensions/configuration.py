import os
import random
import string

from dynaconf import FlaskDynaconf

flask_dynaconf = FlaskDynaconf()


def init_app(app, **config):
    env_vars = ('SECRET_KEY',)

    for env_var in env_vars:
        if env_var not in app.config:
            random_secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
            app.config[env_var] = os.environ.get(env_var, random_secret_key)

    flask_dynaconf.init_app(app, **config)
    app.config.load_extensions()
