from pyblog.extensions.database import db

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id')),
    db.Index('uix_followers', "follower_id", "followed_id", unique=True)
)
