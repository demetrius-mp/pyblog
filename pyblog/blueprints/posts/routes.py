from flask import Blueprint, render_template, flash, redirect, url_for

from pyblog.blueprints.posts.forms import CreatePostForm
from pyblog.blueprints.user.forms import RegistrationForm, LoginForm, ForgotPasswordForm
from pyblog.extensions import auth
from pyblog.extensions.database import get_session
from pyblog.models import Post

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
        unavailable_slugs = list(map(lambda p: p.slug, auth.current_user.posts))
        post.slug = Post.generate_valid_slug(post.title, unavailable_slugs)
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


@posts.route('/edit/<string:post_slug>', methods=['GET', 'POST'])
@auth.login_required
def edit(post_slug: str):
    post: Post = Post.query.filter_by(slug=post_slug).first()
    if not post or post.user_id != auth.current_user.id:
        flash('Post not found', 'error')
        return redirect(url_for('main.index'))

    form = CreatePostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.content = form.content.data
        post.is_published = form.publish.data
        session = get_session()
        session.add(post)
        session.commit()

        if form.publish.data:
            flash('Post published sucessfully!', category='success')
        elif form.save_draft.data:
            flash('Post edited succesfully!', category='info')

        return redirect(url_for('main.index'))

    else:
        for k, v in form.errors.items():
            for error in v:
                flash(error, category='warning')

    form.title.data = post.title
    form.description.data = post.description
    form.content.data = post.content

    return render_template('posts/new.html', title='Edit post', form=form,
                           post=post)


@posts.route('/<string:username>/<string:post_slug>')
def view(username: str, post_slug: str):
    post: Post = Post.query.filter_by(slug=post_slug).first()
    if not post or post.user.username != username:
        flash('Post not found.', 'error')
        return redirect(url_for('main.index'))

    forgot_password_form = ForgotPasswordForm()
    registration_form = RegistrationForm()
    login_form = LoginForm()

    return render_template('posts/view.html', title='Post', post=post,
                           forgot_password_form=forgot_password_form,
                           registration_form=registration_form, login_form=login_form)
