from flask import render_template, Blueprint, request, redirect

from pyblog.blueprints.main.forms import SearchForm
from pyblog.blueprints.user.forms import RegistrationForm, LoginForm, ForgotPasswordForm
from pyblog.extensions import auth
from pyblog.models import Post

main = Blueprint('main', __name__)


@main.route("/", methods=['GET'])
def index():
    next_page = request.args.get('next')
    if next_page:
        return redirect(next_page)

    search_query = request.args.get('search')
    search_form = SearchForm()

    if search_query:
        search_form.search.data = search_query
        search_query = f'%{search_query}%'
        # noinspection PyUnresolvedReferences
        posts: list[Post] = Post.query.filter(Post.title.like(search_query)).all()

    else:
        posts: list[Post] = Post.query.filter_by(is_published=True).all()

    recommended_posts: list[Post] = (
        Post.query.filter_by(is_published=True)
            .order_by(Post.id).limit(3).all()
    )

    if auth.current_user.is_authenticated:
        return render_template('index.html', title='Home', posts=posts,
                               recommended_posts=recommended_posts,
                               search_form=search_form)

    forgot_password_form = ForgotPasswordForm()
    registration_form = RegistrationForm()
    login_form = LoginForm()

    return render_template('index.html', title='Home',
                           forgot_password_form=forgot_password_form,
                           registration_form=registration_form,
                           login_form=login_form, posts=posts,
                           recommended_posts=recommended_posts,
                           search_form=search_form)
