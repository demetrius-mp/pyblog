from datetime import datetime

from flask import Blueprint, render_template

from pyblog.ext import auth
from pyblog.blueprints.posts.forms import CreatePostForm
from pyblog.models import Post

posts = Blueprint('posts', __name__)


@posts.route('/new', methods=['GET', 'POST'])
@auth.login_required
def new():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

    now = datetime.utcnow().strftime('%d/%m/%Y at %H:%M:%S')
    return render_template('new_post.html', title='Create Post', now=now)
