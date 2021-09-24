from flask import render_template, Blueprint, request, redirect

from pyblog.blueprints.user.forms import RegistrationForm, LoginForm
from pyblog.models import Post

main = Blueprint('main', __name__)


@main.route("/", methods=['GET'])
def index():
    next_page = request.args.get('next')
    if next_page:
        return redirect(next_page)

    registration_form = RegistrationForm()
    login_form = LoginForm()

    posts: list[Post] = Post.query.filter_by(is_published=True).all()
    recommended_posts: list[Post] = (
        Post.query.filter_by(is_published=True)
            .order_by(Post.id).limit(3).all()
    )

    return render_template('index.html', title='Home',
                           registration_form=registration_form,
                           login_form=login_form, posts=posts,
                           recommended_posts=recommended_posts)
