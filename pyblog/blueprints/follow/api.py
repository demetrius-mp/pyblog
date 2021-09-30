from functools import wraps

from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

from pyblog.extensions import auth
from pyblog.extensions.database import get_session
from pyblog.models import User
from pyblog.blueprints.api_decorators import login_required_api

api = Blueprint('follows_api', __name__, url_prefix='/api/follows')


def user_must_exist(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = User.query.filter_by(username=kwargs['username']).first()
        if not user:
            return jsonify({
                'msg': 'User not found.',
                'category': 'info'
            }), 404
        return f(*args, **kwargs, followed_user=user)
    return decorated_function


# noinspection PyUnusedLocal
@api.post('/<string:username>')
@user_must_exist
@login_required_api
def follow(username: str, followed_user: User):
    auth.current_user.follow(followed_user)
    session = get_session()
    session.add(auth.current_user)

    try:
        session.commit()
    except IntegrityError:
        return jsonify({
            'msg': 'You are already following this user.',
            'category': 'error'
        }), 400

    return jsonify({
        'msg': 'User followed successfully!',
        'category': 'success'
    })


# noinspection PyUnusedLocal
@api.delete('/<string:username>')
@user_must_exist
@login_required_api
def unfollow(username: str, followed_user: User):
    auth.current_user.unfollow(followed_user)
    session = get_session()
    session.add(auth.current_user)

    try:
        session.commit()
    except StaleDataError:
        return jsonify({
            'msg': 'You are not following this user.',
            'category': 'error'
        }), 400

    return jsonify({
        'msg': 'User unfollowed successfully!',
        'category': 'success'
    })
