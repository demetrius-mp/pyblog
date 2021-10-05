from flask import render_template, Blueprint, request, redirect
from sqlalchemy import func, desc, and_

from pyblog.blueprints.main.forms import SearchForm
from pyblog.blueprints.user.forms import RegistrationForm, LoginForm, ForgotPasswordForm
from pyblog.extensions import auth
from pyblog.extensions.database import get_session
from pyblog.models import Post, Like

main = Blueprint('main', __name__)


@main.route("/", methods=['GET'])
def index():
    """Route to the home page."""
    next_page = request.args.get('next')
    if next_page:
        return redirect(next_page)

    search_query = request.args.get('search')
    search_form = SearchForm()

    page = request.args.get('page', 1, type=int)
    if search_query:
        search_form.search.data = search_query
        search_query = f'%{search_query}%'
        # noinspection PyUnresolvedReferences
        posts: list[Post] = Post.query\
            .filter(and_(Post.title.like(search_query), Post.is_published))\
            .paginate(page=page, per_page=5)

    else:
        posts: list[Post] = Post.query.filter_by(is_published=True)\
            .paginate(page=page, per_page=5)

    session = get_session()
    recommended_posts: list[Post] = session.query(Post) \
        .outerjoin(Like).group_by(Post.id).order_by(desc(func.count(Like.post_id))).limit(3).all()
    session.close()

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
