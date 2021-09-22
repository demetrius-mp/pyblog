from pyblog.ext.database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512))
    full_name = db.Column(db.String(100))
    bio = db.Column(db.String(150))
    # currently_learning = db.Column(db.String(25))
