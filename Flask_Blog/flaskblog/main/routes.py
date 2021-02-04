from flask import render_template, request, Blueprint
from flaskblog.models import Post
import json
from flaskblog.main.forms import SpotifyForm
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("home.html", posts=posts)

@main.route("/spotify")
@login_required
def spotify():
    form = SpotifyForm()
    return render_template('spotify.html', title="Spotify", form=form)