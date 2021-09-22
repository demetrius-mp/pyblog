from flask import Flask

from pyblog.blueprints.user.routes import users as bp


def init_app(app: Flask):
    app.register_blueprint(bp)
