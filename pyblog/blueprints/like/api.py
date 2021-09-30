from flask import Blueprint, jsonify

from pyblog.extensions import auth
from pyblog.extensions.database import get_session
from pyblog.models import Like, Post

api = Blueprint('likes_api', __name__, url_prefix='/api/likes')


@api.post('/<int:post_id>')
@auth.login_required
def like_post(post_id: int):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({
            'msg': 'Post not found.',
            'category': 'info'
        }), 404

    like = Like(user_id=auth.current_user.id, post_id=post.id)
    session = get_session()
    session.add(like)
    session.commit()

    return jsonify({
        'msg': 'Post liked successfully',
        'category': 'success'
    })


@api.delete('/<int:post_id>')
@auth.login_required
def dislike_post(post_id: int):
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
