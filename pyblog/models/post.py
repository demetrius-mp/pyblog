from datetime import datetime

from pyblog.extensions.database import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    title = db.Column(db.String(60), nullable=False)
    slug = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    posted_in = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', back_populates='posts')
