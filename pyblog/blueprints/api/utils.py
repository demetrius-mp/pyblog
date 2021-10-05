from functools import wraps

from flask import jsonify

from pyblog.extensions import auth


def login_required_api(f):
    """Requires that the current user is logged in to do the request."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = auth.current_user
        if not current_user.is_authenticated:
            return jsonify({
                'msg': 'You must login first.',
                'category': 'info'
            }), 401
        return f(*args, **kwargs)
    return decorated_function
