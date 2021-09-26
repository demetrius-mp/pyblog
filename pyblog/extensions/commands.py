from flask import Flask

from pyblog.extensions.database import get_session
from pyblog.models import User


def init_app(app: Flask):
    # add a single command
    @app.cli.command()
    def remove_inactive_users():
        """Removes all inactive users."""
        User.query.filter_by(is_active=False).delete()
        get_session().commit()
