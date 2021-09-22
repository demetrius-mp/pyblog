from pyblog.ext.database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512))
    full_name = db.Column(db.String(100), default='Not provided')
    bio = db.Column(db.String(150), default='Not provided')
    currently_learning = db.Column(db.String(25), default='Not provided')
    experience_in = db.Column(db.String(25), default='Not provided')
    looking_to = db.Column(db.String(25), default='Not provided')
    profile_picture = db.Column(db.String(20), default='default.jpg')
