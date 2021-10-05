from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from wtforms.widgets import TextArea

from pyblog.extensions import auth
from pyblog.models import User


class RegistrationForm(FlaskForm):
    """Form to register a user."""
    username = StringField('Username', id='r_username',
                           validators=[DataRequired(),
                                       Length(min=3, max=30,
                                              message='Username must be between 2 and 30 characters long.')])
    email = StringField('Email', id='r_email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='r_password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up', id='r_submit')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        """Validates that the username is not taken."""
        user = User.query.filter_by(username=username.data).first()
        if user and user.is_active:
            raise ValidationError('That username is taken. Please choose a different one.')

        elif user and not user.is_active:
            raise ValidationError('An inactive account is using this username. '
                                  'Please, wait ~10 mins. or choose a different one')

    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        """Validates that the email is not taken."""
        user = User.query.filter_by(email=email.data).first()
        if user and user.is_active:
            raise ValidationError('That email is taken. Please choose a different one.')

        elif user and not user.is_active:
            raise ValidationError('An account confirmation email was already sent to this email.')


class LoginForm(FlaskForm):
    """Form to login a user."""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    """Form to update an user's profile."""
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    bio = StringField('Bio', validators=[DataRequired(), Length(min=0, max=150)], widget=TextArea())
    full_name = StringField('Full name', validators=[DataRequired(), Length(min=1, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    currently_learning = HiddenField('Currently learning',
                                     validators=[InputRequired(message='Currently learning field can\'t be empty'),
                                                 Length(min=1, max=30)])
    experience_in = HiddenField('Experience in',
                                validators=[InputRequired(message='Experience in field can\'t be empty'),
                                            Length(min=1, max=30)])
    looking_to = HiddenField('Looking to', validators=[InputRequired(message='Looking to field can\'t be empty'),
                                                       Length(min=1, max=30)])
    submit = SubmitField('Confirm changes')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        """Validates that the username is not taken, if it changed."""
        if username.data != auth.current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        """Validates that the email is not taken, if it changed."""
        if email.data != auth.current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    # noinspection PyMethodMayBeStatic
    def validate_currently_learning(self, currently_learning):
        """Validates that the `currently learning` field is not empty."""
        if currently_learning.data.strip() == '':
            raise ValidationError('You can\'t leave the "Currently learning" field empty.')

    # noinspection PyMethodMayBeStatic
    def validate_experience_in(self, experience_in):
        """Validates that the `experience in` field is not empty."""
        if experience_in.data.strip() == '':
            raise ValidationError('You can\'t leave the "Experience in" field empty.')

    # noinspection PyMethodMayBeStatic
    def validate_looking_to(self, looking_to):
        """Validates that the `looking to` field is not empty."""
        if looking_to.data.strip() == '':
            raise ValidationError('You can\'t leave the "Looking to" field empty.')


class ForgotPasswordForm(FlaskForm):
    """Form to send a reset email to a user that forgot his password."""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request password')


class ResetPasswordForm(FlaskForm):
    """Form to reset a user's password."""
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
