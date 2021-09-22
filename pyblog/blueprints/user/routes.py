from flask import url_for, flash, redirect, Blueprint, request
from pyblog.ext import auth
from pyblog.ext.database import db
from pyblog.models import User
from pyblog.blueprints.user.forms import RegistrationForm, LoginForm

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
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login', 'success')

        return redirect(url_for('main.index'))

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
        if user and auth.check_password_hash(user.password, form.password.data):
            auth.login_user(user, remember=form.remember.data)
            flash('Login successful.', 'success')

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.index'))

        else:
            flash('Login unsuccessful. Please check email and password', 'error')

    for k, v in form.errors.items():
        for error in v:
            flash(error, category='warning')

    return redirect(url_for('main.index'))


@users.route('/logout')
@auth.login_required
def logout():
    auth.logout_user()
    flash('Logout succesful', 'success')

    return redirect(url_for('main.index'))
