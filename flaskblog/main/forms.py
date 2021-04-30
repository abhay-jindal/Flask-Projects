from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SpotifyForm(FlaskForm):
    link = StringField("Playlist URI", validators=[DataRequired()])
    submit = SubmitField("Continue")

