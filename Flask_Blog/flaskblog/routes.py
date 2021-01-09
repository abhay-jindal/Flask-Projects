from flask import render_template, url_for, flash, redirect, request, jsonify
from flaskblog import app, db, bcrypt, mail
import secrets, os
from PIL import Image
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, SpotifyForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("home.html", posts=posts)

@app.route("/spotify")
@login_required
def spotify():
    form = SpotifyForm()
    return render_template('spotify.html', title="Spotify", form=form)

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/account/<int:account_id>", methods=['GET'])
@login_required
def account(account_id):
    form = UpdateAccountForm()
    user = User.query.get_or_404(account_id)
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form, account=user)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been published!", "success")
        return redirect(url_for('home'))
    return render_template("create_post.html", title="New Post", form=form, legend='New Post')

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/V1/validate/account", methods=['POST'])
def _validate_user():
    user = User.query.filter_by(email=request.form['email']).first()
    if user and bcrypt.check_password_hash(user.password, request.form['password']):
        remember = request.form.get('remember', False)
        login_user(user, remember=remember)
        return jsonify({'response': True, "redirect": "/home"})
    return jsonify({'response': False})

@app.route("/V1/register/account", methods=['POST'])
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)

    file_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", file_name)
    old_picture_path = os.path.join(app.root_path, "static/profile_pics", current_user.image_file)
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

@app.route("/V1/update/account", methods=['POST'])
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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
         return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if not user:
        flash('Your reset link expired after 30 minutes due to inactivity.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

