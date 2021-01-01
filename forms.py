from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

from wtforms.validators import Email,EqualTo
from wtforms import PasswordField

class SigninForm(FlaskForm):
    
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
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Please enter a password."),
        ]
    )
    confirm = PasswordField(
        'Confirm The Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    #recaptcha = RecaptchaField()
    submit = SubmitField('Add user')
