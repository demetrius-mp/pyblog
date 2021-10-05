from flask import Flask

from pyblog.blueprints.posts.routes import posts


def init_app(app: Flask):
    app.register_blueprint(posts)
