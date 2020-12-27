from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

from wtforms.validators import Email
from wtforms import PasswordField

class SigninForm(FlaskForm):
    """Sign in for an account."""
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired(message="Please enter a password."),
        ]
    )

    #recaptcha = RecaptchaField()
    submit = SubmitField('Submit')