from functools import wraps

from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

from pyblog.extensions import auth
from pyblog.extensions.database import get_session
from pyblog.models import Like, Post
from pyblog.blueprints.api.utils import login_required_api

api = Blueprint('likes_api', __name__, url_prefix='/api/likes')


def post_must_exist(f):
    """Requires that the post exists."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        post = Post.query.get(kwargs['post_id'])
        if not post:
            return jsonify({
                'msg': 'Post not found.',
                'category': 'info'
            }), 404
        return f(*args, **kwargs)
    return decorated_function


@api.post('/<int:post_id>')
@post_must_exist
@login_required_api
def like_post(post_id: int):
    """Likes the given post as the current user."""
    like = Like(user_id=auth.current_user.id, post_id=post_id)
    session = get_session()
    session.add(like)

    try:
        session.commit()
    except IntegrityError:
        return jsonify({
            'msg': 'You already liked this post.',
            'category': 'error'
        }), 400

    return jsonify({
        'msg': 'Post liked successfully',
        'category': 'success'
    })


@api.delete('/<int:post_id>')
@post_must_exist
@login_required_api
def dislike_post(post_id: int):
    """Dislike the given post as the current user."""
    current_user = auth.current_user
    if not current_user.is_authenticated:
        return jsonify({
            'msg': 'You must login to dislike a post.',
            'category': 'info'
        }), 401

    post = Post.query.get(post_id)
    if not post:
        return jsonify({
            'msg': 'Post not found.',
            'category': 'info'
        }), 404

    like = Like.query.filter_by(user_id=auth.current_user.id, post_id=post.id).first()
    if not like:
        return jsonify({
            'msg': 'You did not like this post.',
            'category': 'error'
        }), 400

    session = get_session()
    session.delete(like)
    session.commit()

    return jsonify({
        'msg': 'Post disliked successfully',
        'category': 'success'
    })
