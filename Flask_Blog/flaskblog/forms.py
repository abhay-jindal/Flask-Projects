from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(" Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField("Log in")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(['png', 'jpg', "jpeg", "gif"])])
    submit = SubmitField("Update")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Publish")

class SpotifyForm(FlaskForm):
    link = StringField("Playlist URI", validators=[DataRequired()])
    category = SelectField('Category', choices = [('playlist', 'Playlist'), ('artist', 'Artist'), ('album', 'Album')])
    submit = SubmitField("Download Tracks")


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Reset Password')
