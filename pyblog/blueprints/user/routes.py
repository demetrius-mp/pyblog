from flask import url_for, flash, redirect, Blueprint
from pyblog.ext import auth
from pyblog.ext.database import db
from pyblog.models import User
from pyblog.blueprints.user.forms import RegistrationForm

users = Blueprint('users', __name__)


@users.route("/register", methods=['POST'])
def register():
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
