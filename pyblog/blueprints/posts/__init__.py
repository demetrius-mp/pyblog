from flask import Flask

from pyblog.blueprints.posts.routes import posts
from pyblog.blueprints.posts.api import api


def init_app(app: Flask):
    app.register_blueprint(posts)
    app.register_blueprint(api)
