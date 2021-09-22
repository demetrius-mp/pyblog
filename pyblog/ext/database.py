from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import Session

db = SQLAlchemy()


def get_session() -> Session:
    return db.session


def init_app(app: Flask):
    db.init_app(app)
    with app.app_context():
        event.listen(db.engine, 'connect', lambda con, rec: con.execute('pragma foreign_keys=ON'))
