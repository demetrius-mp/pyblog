import secrets
from pathlib import Path

from PIL import Image
from flask import current_app, url_for

from pyblog.extensions.mail import send_mail


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
    send_mail('Reset password request', body, email)


def send_activate_account_email(email: str, token: str):
    body = f'''Click the following link to activate your account:
                {url_for('users.activate_account', token=token, _external=True)}'''
    send_mail('Activate account', body, email)
