from flask import Flask

from pyblog.blueprints.posts.routes import posts as bp
from pyblog.blueprints.posts.api import posts_api as bp_api


def init_app(app: Flask):
    app.register_blueprint(bp)
    app.register_blueprint(bp_api)
