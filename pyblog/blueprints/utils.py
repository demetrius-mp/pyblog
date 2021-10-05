from flask import redirect, url_for, flash
from functools import wraps


def disable_route(f):
    """Disables the decorated route, i.e turns it unaccessible."""

    # noinspection PyUnusedLocal
    @wraps(f)
    def decorated_function(*args, **kwargs):
        flash('This route is disabled at the moment!', 'info')
        return redirect(url_for('main.index'))

    return decorated_function
