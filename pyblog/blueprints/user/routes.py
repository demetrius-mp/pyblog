from typing import Iterator

from flask import url_for, flash, redirect, Blueprint, request, render_template

from pyblog.blueprints.user import utils
from pyblog.blueprints.user.forms import RegistrationForm, LoginForm, UpdateProfileForm, ForgotPasswordForm, \
    ResetPasswordForm
from pyblog.extensions import auth
from pyblog.extensions.database import get_session
from pyblog.models import User, Post

users = Blueprint('users', __name__)


@users.route("/register", methods=['POST'])
def register():
    if auth.current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = auth.generate_password_hash(form.password.data)
        # noinspection PyArgumentList
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        session = get_session()
        session.add(user)
        session.commit()
        session.refresh(user)

        token = user.get_reset_token(expires_seconds=600)
        utils.send_activate_account_email(user.email, token)
        utils.delete_non_activated_user(user.id)

        flash('Your account has been created!', 'success')
        flash('Confirm your account by clicking the link we sent in your email.', 'info')

    for k, v in form.errors.items():
        for error in v:
            flash(error, category='warning')

    return redirect(url_for('main.index'))


@users.route("/login", methods=['POST'])
def login():
    if auth.current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and not user.is_active:
            flash('Please, activate your account.', 'warning')
            return redirect(url_for('main.index'))

        if user and auth.check_password_hash(user.password, form.password.data):
            auth.login_user(user, remember=form.remember.data)
            flash('Login successful.', 'success')

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            return redirect(url_for('main.index'))

        else:
            flash('Login unsuccessful. Please check email and password', 'error')

    for k, v in form.errors.items():
        for error in v:
            flash(error, category='warning')

    return redirect(url_for('main.index'))


@users.route('/activate-account/<string:token>', methods=['GET', 'POST'])
def activate_account(token: str):
    if auth.current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user: User = User.verify_reset_token(token)
    if not user:
        flash('Token expired.', 'error')
        return redirect(url_for('main.index'))

    user.is_active = True
    session = get_session()
    session.add(user)
    session.commit()
    session.refresh(user)

    auth.login_user(user)
    flash('Account activated successfully!', 'success')
    return redirect(url_for('users.me'))


@users.route('/forgot-password', methods=['POST'])
def forgot_password():
    if auth.current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user: User = User.query.filter_by(email=email).first()
        if user is None:
            return redirect(url_for('main.index'))

        token = user.get_reset_token()
        utils.send_reset_password_email(user.email, token)
        flash('Reset password email sent successfully!', 'success')

    for k, v in form.errors.items():
        for error in v:
            flash(error, category='warning')

    return redirect(url_for('main.index'))


@users.route('/reset-password/<string:token>', methods=['GET', 'POST'])
def reset_password(token: str):
    if auth.current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user: User = User.verify_reset_token(token)
    if not user:
        flash('Token expired.', 'error')
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = auth.generate_password_hash(form.password.data)
        user.password = hashed_password
        session = get_session()
        session.add(user)
        session.commit()

        flash('Password reset successfully!', 'success')

        return redirect(url_for('main.index'))

    return render_template('users/reset_password.html', form=form)


@users.route('/logout')
@auth.login_required
def logout():
    auth.logout_user()
    flash('Logout succesful', 'success')

    return redirect(url_for('main.index'))


@users.route('/me', methods=['GET', 'POST'])
@auth.login_required
def me():
    current_user: User = auth.current_user
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if not auth.check_password_hash(current_user.password, form.password.data):
            flash('Incorrect password.', 'error')
            return redirect(url_for('users.me'))

        if form.picture.data:
            picture_file = utils.save_picture(form.picture.data)
            current_user.profile_picture = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.full_name = form.full_name.data
        current_user.currently_learning = form.currently_learning.data
        current_user.experience_in = form.experience_in.data
        current_user.looking_to = form.looking_to.data
        session = get_session()
        session.add(current_user)
        session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.me'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        form.bio.data = current_user.bio
        form.full_name.data = current_user.full_name
        form.currently_learning.data = current_user.currently_learning
        form.experience_in.data = current_user.experience_in
        form.looking_to.data = current_user.looking_to

    for error in form.currently_learning.errors:
        flash(error, category='warning')

    for error in form.experience_in.errors:
        flash(error, category='warning')

    for error in form.looking_to.errors:
        flash(error, category='warning')

    return render_template('users/me.html', form=form, title='Me')


@users.route('/<string:username>', methods=['GET', 'POST'])
def user_page(username: str):
    user: User = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found.', 'warning')
        return redirect(url_for('main.index'))

    forgot_password_form = ForgotPasswordForm()
    registration_form = RegistrationForm()
    login_form = LoginForm()

    posts: list[Post] = list(filter(lambda p: p.is_published, user.posts))

    return render_template('users/user_page.html', user=user, posts=posts,
                           title='User', login_form=login_form,
                           registration_form=registration_form,
                           forgot_password_form=forgot_password_form)


@users.route('/dashboard')
@auth.login_required
def dashboard():
    posts = auth.current_user.posts
    draft_posts: Iterator[Post] = list(filter(lambda p: not p.is_published, posts))
    published_posts: Iterator[Post] = list(filter(lambda p: p.is_published, posts))

    return render_template('users/dashboard.html', draft_posts=draft_posts,
                           published_posts=published_posts, title='Dashboard')
