from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SubmitField,
                     PasswordField,
                     BooleanField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                ValidationError)

from app.models import users

class LoginForm(FlaskForm):
    email = StringField('Email : ',
                        [DataRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "inputs", "id": "email", "required": ''})
    password = PasswordField('Password : ', [DataRequired()], render_kw={
                             "placeholder": "Password", "class": "inputs", "id": "password", "required": ''})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    username = StringField('Username : ',
                           [DataRequired()], render_kw={"placeholder": "Username", "class": "inputs", "id": "username"})

    email = StringField('Email : ',
                        [DataRequired(), Email()], render_kw={"placeholder": "Email", "class": "inputs", "id": "email"})

    name = StringField('Name : ', [DataRequired()], render_kw={
                       "placeholder": "Name", "class": "inputs", "id": "name"})

    password = PasswordField('Password : ', [DataRequired()], render_kw={
                             "placeholder": "Password", "class": "inputs", "id": "password"})
    confirm_password = PasswordField('Confirm Password : ',
                                     validators=[DataRequired(), EqualTo('password')], render_kw={
                                         "placeholder": "Confirm Password", "class": "inputs", "id": "confirm_password"})
    auth_code = StringField('Authentication Code : ', [DataRequired()], render_kw={"placeholder":"Authentication Code : ", "class":"inputs", "id":"auth_code"})

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class AccountForm(FlaskForm):
    username = StringField('Username', render_kw={
                           "placeholder": "Username", "class": "inputs", "id": "username", "disabled": ''})

    email = StringField('Email',
                        [DataRequired(), Email()], render_kw={"placeholder": "Email", "class": "inputs", "id": "email"})

    name = StringField('Name : ',  render_kw={
                       "placeholder": "Name", "class": "inputs", "id": "name", "disabled": ''})

    old_password = PasswordField('Old Password', [DataRequired()], render_kw={
        "placeholder": "Old Password", "class": "inputs", "id": "old_password"})
    new_password = PasswordField('New Password',
                                 validators=[DataRequired()], render_kw={
                                     "placeholder": "New Password", "class": "inputs", "id": "new_password"})
    submit = SubmitField('Update')