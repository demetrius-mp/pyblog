import secrets
from datetime import timedelta
from pathlib import Path

from PIL import Image
from flask import current_app, url_for, Flask

from pyblog.extensions import mail
from pyblog.extensions.database import get_session
from pyblog.extensions.scheduler import add_one_time_job
from pyblog.models import User


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)

    picture_extension = Path(form_picture.filename).suffix
    picture_filename = random_hex + picture_extension
    picture_path = Path(current_app.root_path) / 'static' / 'profile_pics' / picture_filename

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename


def send_reset_password_email(email: str, token: str):
    body = f'''To reset your password, visit the following link:
                {url_for('users.reset_password', token=token, _external=True)}'''
    mail.send_email('Reset password request', body, email)


def send_activate_account_email(email: str, token: str):
    body = f'''Click the following link to activate your account:
                {url_for('users.activate_account', token=token, _external=True)}'''
    mail.send_email('Activate account', body, email)


def delete_non_activated_user(user_id: int, delete_after: timedelta = timedelta(minutes=10)):
    def func(app_: Flask, user_id_: int):
        with app_.app_context():
            user = User.query.get(user_id_)
            if user and not user.is_active:
                session = get_session()
                session.delete(user)
                session.commit()

    # noinspection PyUnresolvedReferences,PyProtectedMember
    app = current_app._get_current_object()
    add_one_time_job(func, (app, user_id), delete_after)
