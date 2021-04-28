from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, TimeField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ReminderForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=12)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=12)])
    email = StringField("Email", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    reminder_date = DateField('Reminder Date', validators=[DataRequired()])
    reminder_time = TimeField('Reminder Time', validators=[DataRequired()])
    submit = SubmitField("Set Reminder")

