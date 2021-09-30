from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

from pyblog.extensions import auth
from pyblog.extensions.database import get_session
from pyblog.models import Like, Post

api = Blueprint('likes_api', __name__, url_prefix='/api/likes')


# noinspection DuplicatedCode
@api.post('/<int:post_id>')
def like_post(post_id: int):
    current_user = auth.current_user
    if not current_user.is_authenticated:
        return jsonify({
            'msg': 'You must login to like a post.',
            'category': 'info'
        }), 401

    post = Post.query.get(post_id)
    if not post:
        return jsonify({
            'msg': 'Post not found.',
            'category': 'info'
        }), 404

    like = Like(user_id=current_user.id, post_id=post.id)
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


# noinspection DuplicatedCode
@api.delete('/<int:post_id>')
def dislike_post(post_id: int):
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
    session = get_session()
    session.delete(like)
    session.commit()

    return jsonify({
        'msg': 'Post disliked successfully',
        'category': 'success'
    })
