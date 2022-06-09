from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from werkzeug.security import check_password_hash

from app.models import User


class RegisterForm(FlaskForm):

    username = StringField(label='Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField(label='Password', validators=[DataRequired()])
    rpassword = PasswordField(label='Repeat password', validators=[DataRequired(),
                                                                   EqualTo('password',
                                                                           message='Password don`t match')])
    email = EmailField(label='Email', validators=[DataRequired(), Email()])

    def validate_email(self, email):
        existent = User.query.filter_by(email=email.data).first()
        if existent:
            raise ValidationError('This email already register!')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('This username already register')


class LoginForm(FlaskForm):

    email = EmailField(label='Email', validators=[Email()])
    password = PasswordField(label='Password')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if not user or not check_password_hash(user.password, password.data):
            raise ValidationError('Email or password is wrong')


class PostForm(FlaskForm):

    title = StringField(label='title', validators=[DataRequired()])
    body = TextAreaField(label='body', validators=[DataRequired()])

