import secrets
from pathlib import Path

from flask import current_app
from PIL import Image


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
