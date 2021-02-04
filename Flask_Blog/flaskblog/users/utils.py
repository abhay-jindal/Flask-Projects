import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
from flask_login import current_user

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)

    file_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", file_name)
    old_picture_path = os.path.join(current_app.root_path, "static/profile_pics", current_user.image_file)
    try:
        if current_user.image_file != 'default.png':
            os.remove(old_picture_path)
    except Exception as e:
        pass

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return file_name

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)