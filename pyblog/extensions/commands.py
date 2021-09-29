import datetime
from pathlib import Path

from flask import Flask
import json
# noinspection PyPackageRequirements
from slugify import slugify

from pyblog.extensions.database import get_session
from pyblog.models import User, Post


def add_dummy_data_():
    dummy_data_folder = Path(__file__).parent.parent / 'fakedata'
    session = get_session()

    dummy_users: list[dict]
    with open(dummy_data_folder / 'users.json', 'r') as f:
        dummy_users = json.load(f)

    db_users: list[User] = []
    for dummy_user in dummy_users:
        # noinspection PyArgumentList
        db_user = User(
            username=dummy_user['username'],
            password=dummy_user['password'],
            full_name=dummy_user['name'],
            email=dummy_user['mail'],
            looking_to=dummy_user['looking_to'],
            experience_in=dummy_user['experience_in'],
            currently_learning=dummy_user['currently_learning'],
            is_active=dummy_user['is_active'],
            bio=dummy_user['bio'],
        )

        db_users.append(db_user)

    session.add_all(db_users)

    dummy_posts: list[dict]
    with open(dummy_data_folder / 'posts.json', 'r') as f:
        dummy_posts = json.load(f)

    db_posts: list[Post] = []
    for dummy_post in dummy_posts:
        # noinspection PyArgumentList
        db_post = Post(
            user_id=dummy_post['user_id'],
            title=dummy_post['title'],
            slug=slugify(dummy_post['title']),
            is_published=True,
            description=dummy_post['description'],
            content=dummy_post['content'],
            posted_in=datetime.datetime.utcnow()
        )

        db_posts.append(db_post)

    session.add_all(db_posts)

    session.commit()


def init_app(app: Flask):
    @app.cli.command()
    def add_dummy_data():
        """Adds dummy users and posts to the blog"""
        add_dummy_data_()
