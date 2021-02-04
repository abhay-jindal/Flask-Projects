from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@users.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))

@users.route("/account/<int:account_id>", methods=['GET'])
@login_required
def account(account_id):
    form = UpdateAccountForm()
    user = User.query.get_or_404(account_id)
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form, account=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
         return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('users.login'))
        else:
            flash('That address is not a verified primary email or is not associated with a personal user account.', 'danger')
            return redirect(url_for('users.reset_request'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
         return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if not user:
        flash('Your reset link expired after 30 minutes due to inactivity.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/V1/validate/account", methods=['POST'])
def _validate_user():
    user = User.query.filter_by(email=request.form['email']).first()
    if user and bcrypt.check_password_hash(user.password, request.form['password']):
        remember = request.form.get('remember', False)
        login_user(user, remember=remember)
        return jsonify({'response': True, "redirect": "/home"})
    return jsonify({'response': False})

@users.route("/V1/register/account", methods=['POST'])
def _register_user():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'response': False, "error": "Email already registered. Choose another email!"})
    else:
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=request.form['username'], email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return jsonify({'response': True, "redirect": "/login"})


@users.route("/V1/update/account", methods=['POST'])
def _update_user():
    email = request.form['email']
    picture = request.files['picture']
    username = request.form['username']
    already_user = User.query.filter_by(email=email).first()
    if already_user and already_user.username == username and not picture:
        return jsonify({'response': False, "error": "Email already registered. Choose another email!"})

    image = ""
    user = User.query.filter_by(email=request.form['current_email']).first()
    user.username = username
    user.email = email
    if picture:
        picture_file = save_picture(picture)
        user.image_file = picture_file
        image = url_for('static', filename='profile_pics/' + user.image_file)
    db.session.commit()
    return jsonify({'response': True, 'image': image})
