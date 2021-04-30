from flask import Blueprint, render_template

books = Blueprint('books', __name__)

@books.route("/books")
def get_isbn_info():
    return render_template('isbn_info.html', title='Book Store')