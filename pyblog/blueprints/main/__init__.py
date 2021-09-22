from flask import Flask

from pyblog.blueprints.main.routes import main as bp


def init_app(app: Flask):
    app.register_blueprint(bp)
