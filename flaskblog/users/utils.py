import os
import secrets
from PIL import Image
from flask import url_for, current_app, render_template
from flask_mail import Message
from flaskblog import mail
from flask_login import current_user

def picture_path_exists(picture):
    picture_path = os.path.join(current_app.root_path, "static\profile_pics", picture.split("/")[3])
    if os.path.exists(picture_path):
        return True
    else:
        return False

def save_default_picture():
    import shutil

    default_picture = os.path.join(current_app.root_path, "static\profile_pics", "default.png")
    file_name = secrets.token_hex(8) + ".png"
    new_picture = os.path.join(current_app.root_path, "static\profile_pics", file_name)
    shutil.copy(default_picture, new_picture)
    return file_name
    
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

def send_async_email(current_app, message):
    with current_app.app_context():
        mail.send(message)

def send_reset_email(user):
    from threading import Thread

    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.html = render_template('reset_password.html', user=user, token=token)
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg,)).start()
