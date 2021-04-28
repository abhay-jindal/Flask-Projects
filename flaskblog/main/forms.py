from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SpotifyForm(FlaskForm):
    link = StringField("Playlist URI", validators=[DataRequired()])
    category = SelectField('Category', choices = [('playlist', 'Playlist'), ('artist', 'Artist'), ('album', 'Album')])
    submit = SubmitField("Download Tracks")

