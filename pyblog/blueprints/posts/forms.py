from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


class CreatePostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=2, max=30)])
    description = StringField('Description', validators=[DataRequired(), Length(min=10, max=300)], widget=TextArea())
    content = StringField('Content',
                          validators=[Length(min=10, message='Content field must have at least 10 characters')],
                          widget=TextArea())

    save_draft = SubmitField('Save draft')
    publish = SubmitField('Publish')
