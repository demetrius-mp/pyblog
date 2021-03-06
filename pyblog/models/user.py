from __future__ import annotations

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import SignatureExpired

from pyblog.extensions.database import db
from pyblog.models.follow import followers


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
    profile_picture = db.Column(db.String(255), default='default.jpg')
    is_active = db.Column(db.Boolean, default=False)

    posts = db.relationship('Post', back_populates='user')
    likes = db.relationship('Like', back_populates='user')
    # noinspection PyPropertyAccess
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def follow(self, user):
        self.followed.append(user)

    def unfollow(self, user):
        self.followed.remove(user)

    # noinspection PyPropertyAccess
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id)\
                   .count() > 0

    def get_reset_token(self, expires_seconds: int = 18000) -> str:
        secret_key = current_app.config.secret_key
        s = Serializer(secret_key, expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token: str) -> User | None:
        secret_key = current_app.config.secret_key
        s = Serializer(secret_key)
        try:
            user_id: int = s.loads(token)['user_id']
        except SignatureExpired:
            return None

        return User.query.get(user_id)
