from flask import Blueprint, jsonify
from pyblog.models import Post

api = Blueprint('posts_api', __name__, url_prefix='/api/posts')


@api.get('/<int:post_id>')
def get_one(post_id: int):
    post: Post = Post.query.get(post_id)
    return jsonify(post.content)
