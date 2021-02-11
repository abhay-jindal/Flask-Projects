from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from flaskblog.reminder.forms import ReminderForm

reminder = Blueprint('reminder', __name__)

@reminder.route("/set-reminder/", methods=['GET', 'POST'])
@login_required
def set_reminder():
    form = ReminderForm()
    if request.method == 'GET':
        form.email.data = current_user.email

    elif request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        message = request.form['message']
        reminder_date = request.form['reminder_date']
        reminder_time = request.form['reminder_time']
        flash("Message has been scheduled! Reminder will be sent prior 30 minutes to your scheduled time.", "info")
        return redirect(url_for('main.home'))
    return render_template('reminder.html', form=form)