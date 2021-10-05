from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """Form to search for posts."""
    search = StringField('Search', validators=[DataRequired()])
