from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    with app.app_context():
        event.listen(db.engine, 'connect', lambda con, rec: con.execute('pragma foreign_keys=ON'))
