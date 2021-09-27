import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import Session

db = SQLAlchemy()


def get_session() -> Session:
    return db.session


def init_app(app: Flask):
    env_vars = ('SQLALCHEMY_DATABASE_URI',)

    for env_var in env_vars:
        if env_var not in app.config:
            app.config[env_var] = os.environ.get(env_var)

    db.init_app(app)
    with app.app_context():
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            event.listen(db.engine, 'connect', lambda con, rec: con.execute('pragma foreign_keys=ON'))
