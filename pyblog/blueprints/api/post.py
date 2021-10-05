from flask import Blueprint, jsonify
from pyblog.models import Post

api = Blueprint('posts_api', __name__, url_prefix='/api/posts')


@api.get('/<string:post_slug>')
def get_one(post_slug: str):
    """Returns a single post, if it exists."""
    post: Post = Post.query.filter_by(slug=post_slug).first()
    return jsonify(post.content)
