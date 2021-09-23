from flask import Blueprint, render_template, flash, redirect, url_for
# noinspection PyPackageRequirements
from slugify import slugify

from pyblog.blueprints.posts.forms import CreatePostForm
from pyblog.extensions import auth
from pyblog.extensions.database import get_session
from pyblog.models import Post, User

posts = Blueprint('posts', __name__)


@posts.route('/new', methods=['GET', 'POST'])
@auth.login_required
def new():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post()
        post.user_id = auth.current_user.id
        post.title = form.title.data
        post.description = form.description.data
        post.content = form.content.data
        post.is_published = form.publish.data
        post.slug = slugify(post.title, max_length=256)
        session = get_session()
        session.add(post)
        session.commit()

        if form.publish.data:
            flash('Post published succesfully!', 'success')
            return redirect(url_for('users.user_page', username=auth.current_user.username))

        elif form.save_draft.data:
            flash('Saved post draft.', 'info')

        return redirect(url_for('main.index'))

    for k, v in form.errors.items():
        for error in v:
            flash(error, category='warning')

    return render_template('posts/new.html', title='Create Post', form=form)


@posts.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@auth.login_required
def edit(post_id: int):
    post: Post = Post.query.get(post_id)
    if not post or post.user_id != auth.current_user.id:
        flash('Post not found', 'error')
        return redirect(url_for('main.index'))

    form = CreatePostForm()
    form.title.data = post.title
    form.description.data = post.description
    form.content.data = post.content

    return render_template('posts/new.html', title='Edit post', form=form,
                           post=post)
