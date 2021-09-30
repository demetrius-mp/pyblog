from pyblog.extensions.database import db


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'))

    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')

    __table_args__ = (db.Index('uix_likes', "user_id", "post_id", unique=True),)
