from flask import Flask

from pyblog.blueprints.api import follow, like, post


def init_app(app: Flask):
    app.register_blueprint(follow.api)
    app.register_blueprint(like.api)
    app.register_blueprint(post.api)
