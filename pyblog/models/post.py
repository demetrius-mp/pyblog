from datetime import datetime

# noinspection PyPackageRequirements
from slugify import slugify

from pyblog.ext.database import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    title = db.Column(db.String(60), nullable=False)
    slug = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_draft = db.Column(db.Boolean, nullable=False, default=True)
    posted_in = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', back_populates='posts')

    def __init__(self, *args, **kwargs):
        if 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))
        super().__init__(*args, **kwargs)
