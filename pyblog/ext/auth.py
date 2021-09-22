from flask import Flask
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from pyblog.models import User

login_manager = LoginManager()

login_user = login_user
logout_user = logout_user
login_required = login_required
current_user = current_user

generate_password_hash = generate_password_hash
check_password_hash = check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_app(app: Flask):
    login_manager.init_app(app)
