from flask import render_template, Blueprint, request, redirect

from pyblog.blueprints.user.forms import RegistrationForm, LoginForm

main = Blueprint('main', __name__)


@main.route("/", methods=['GET'])
def index():
    registration_form = RegistrationForm()
    login_form = LoginForm()

    next_page = request.args.get('next')
    if next_page:
        return redirect(next_page)

    return render_template('index.html', title='Home',
                           registration_form=registration_form,
                           login_form=login_form)
