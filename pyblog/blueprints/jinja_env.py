from datetime import datetime

from flask import Flask


def init_app(app: Flask):
    def utc_now():
        return datetime.utcnow().strftime('%d/%m/%Y at %H:%M:%S')

    app.jinja_env.globals.update(utc_now=utc_now)
