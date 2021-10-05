from datetime import datetime

from flask import Flask


def init_app(app: Flask):
    """Adds jinja global functions and variables."""
    def utc_now():
        return datetime.utcnow().strftime('%d/%m/%Y at %H:%M:%S')

    def format_date(date: datetime):
        return date.strftime('%d/%m/%Y at %H:%M:%S')

    app.jinja_env.globals.update(utc_now=utc_now, format_date=format_date)
