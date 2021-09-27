import os
import random
import string

from flask import Flask

from pyblog.extensions import configuration


def create_app():
    app = Flask(__name__)
    configuration.init_app(app)
    random_secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
    app.secret_key = os.environ.get('SECRET_KEY', random_secret_key)

    return app
