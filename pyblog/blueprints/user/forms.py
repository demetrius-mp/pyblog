from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from pyblog.models import User
from pyblog.ext import auth


class RegistrationForm(FlaskForm):
    username = StringField('Username', id='r_username',
                           validators=[DataRequired(),
                                       Length(min=2, max=30,
                                              message='Username must be between 2 and 20 characters long.')])
    email = StringField('Email', id='r_email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='r_password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up', id='r_submit')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    bio = StringField('Bio', validators=[DataRequired(), Length(min=0, max=150)], widget=TextArea())
    full_name = StringField('Full name', validators=[DataRequired(), Length(min=1, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm changes')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        if username.data != auth.current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        if email.data != auth.current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
