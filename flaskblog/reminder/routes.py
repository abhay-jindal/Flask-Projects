from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user
from flaskblog.reminder.forms import ReminderForm
from flaskblog import create_app


reminder = Blueprint('reminder', __name__)

@reminder.route("/set-reminder/", methods=['GET', 'POST'])
def set_reminder():
    form = ReminderForm()
    if request.method == 'GET' and current_user.is_authenticated:
        form.email.data = current_user.email

    elif request.method == 'POST':
        data = {}
        data['email'] = request.form['email']
        data['first_name'] = request.form['first_name']
        data['last_name'] = request.form['last_name']
        data['message'] = request.form['message']
        reminder_date = request.form['reminder_date']
        reminder_time = request.form['reminder_time']
       
        send_mail.apply_async(args=[data], countdown=60)
        flash("Message has been scheduled! Reminder will be sent prior 30 minutes to your scheduled time.", "info")
        return redirect(url_for('main.home'))
    return render_template('reminder.html', form=form)

# celery_client = Celery(current_app._get_current_object().name, broker=current_app.config['CELERY_BROKER_URL'])
# celery_client.conf.update(current_app.config)