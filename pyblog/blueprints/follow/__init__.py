from flask import Flask

from pyblog.blueprints.follow.api import api


def init_app(app: Flask):
    app.register_blueprint(api)
