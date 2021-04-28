from flask import Blueprint, render_template
from flask_login import login_required

books = Blueprint('books', __name__)

@books.route("/books")
@login_required
def get_isbn_info():
    return render_template('isbn_info.html', title='Sell Books')