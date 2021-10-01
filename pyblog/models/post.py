from datetime import datetime
import secrets

# noinspection PyPackageRequirements
from slugify import slugify

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

    user = db.relationship('User', back_populates='posts', lazy='joined')
    likes = db.relationship('Like', back_populates='post', lazy='joined')

    @staticmethod
    def generate_valid_slug(title: str, unavailable_slugs: list[str]) -> str:
        slug = slugify(title, max_length=248)
        random_suffix = secrets.token_urlsafe(8)
        complete_slug = slug + random_suffix
        while complete_slug in unavailable_slugs:
            random_suffix = secrets.token_urlsafe(8)
            complete_slug = slug + random_suffix

        return complete_slug
