import os
import requests
import json

from flask import Flask, session, render_template, request, jsonify, url_for, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, BooleanField, StringField, PasswordField, validators

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# First page, before login
@app.route("/")
@login_required
def index():
    pass
    """ Index Page """
    return render_template("index.html")


# Set up register function
# RegistrationForm defined in models.py
# User defined in models.py
@app.route('/register', methods=["GET", "POST"])
def register():
    """ Register User """
    session.clear()
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():

        if not request.form.get("username"):
            flash("Username missing")
            return render_template("register.html")

        # Check if username is already taken
        check_user = db.execute("SELECT * FROM users WHERE username = :username",
        {"username":request.form.get("username")}).fetchone()

        if check_user:
            flash("Username already exists")
            return render_template("register.html")

        elif not request.form.get("password"):
            flash("Password missing")
            return redirect("/register")

        # If username is not taken, create account and redirect to login
        if not check_user:

            # Define secure password using werkzeug
            hashed_password = generate_password_hash(request.form.get("password"), method="sha256")

            # Insert new user information into the databse
            db.execute("INSERT INTO users (username, name, password) VALUES (:username, :name, :password)",
            {"username":request.form.get("username"), "name":request.form.get("name"), "password":hashed_password})
            db.commit()

            # Redirect to login
            flash("Thanks for registering")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)


# Set up login function
@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login User """
    session.clear()
    username = request.form.get("username")

    if request.method == "POST":

        # Check if username was submitted in form
        if not request.form.get("username"):
            flash("Username missing")
            return render_template("login.html")

        # Check if password was submitted in form
        elif not request.form.get("password"):
            flash("Password missing")
            return render_template("login.html")

        # Search the DB for username
        all_users = db.execute("SELECT * FROM users WHERE username = :username", {"username": username})
        result = all_users.fetchone()

        # Check if username and password are correct
        if result == None or not check_password_hash(result[3], request.form.get("password")):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # Remeber user in session
        session["user_id"] = result [0]
        session["user_username"] = result [1]
        session["user_name"] = result [2]
        session["logged_in"] = True

        user_username = session["user_username"]
        user_name = session["user_name"]

        flash("Welcome!")
        # Redirect user to dashboard page
        return render_template("search.html", user_name=session["user_name"])

    # If request.method == "GET"
    else:
        return render_template("login.html")


# Set up Logout function
@app.route("/logout")
@login_required
def logout():
    pass
    """ Logout User """
    session["logged_in"] = False
    session.clear()
    return render_template("logout.html")


# List of all books
@app.route("/books")
@login_required
def books():
    pass
    """ List of all books """
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", books=books)


# Set search bar
@app.route("/search", methods=["GET"])
@login_required
def search():
    pass
    """ Search for books """

    if not request.args.get("book"):
        return render_template("search.html")

    book_search = "%" + request.args.get("book") + "%"
    book_search = book_search.title()
    book_list = db.execute("SELECT * FROM books WHERE title LIKE :book_search OR isbn LIKE :book_search OR author LIKE :book_search", {"book_search":book_search})

    if book_list.rowcount == 0:
        flash("No books matching that description.")
        return render_template("search.html")

    books = book_list.fetchall()
    return render_template("booklist.html", books=books)


# Set profile page
@app.route("/user", methods=["GET"])
@login_required
def user_profile():
    pass
    """ Profile page """
    if request.method == "GET":
        user_name = session["user_name"]
        return render_template("profile.html", user_name=session["user_name"])
    else:
        return redirect("/login")


# Book info - before API - TO CHANGE
#@app.route("/books/<int:book_id>")
#@login_required
#def book(book_id):
#    pass
#    """ Book details """

    # Make sure book exists.
#    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
#    if book is None:
#        flash("There is no such book.")
#        return render_template("books")
#
#    return render_template("book.html", book=book)


###

@app.route("/book/<isbn>", methods=["GET","POST"])
@login_required
def book(isbn):
    """ Save user review and load same page with reviews updated."""

    if request.method == "POST":

        # Save current user info
        currentUser = session["user_id"]

        # Fetch form data
        rating = request.form.get("rating")
        description = request.form.get("description")

        # Search book_id by ISBN
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
                        {"isbn": isbn})

        # Save id into variable
        bookId = row.fetchone() # (id,)
        bookId = bookId[0]

        # Check for user submission (ONLY 1 review/user allowed per book)
        row2 = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
                    {"user_id": currentUser,
                     "book_id": bookId})

        # A review already exists
        if row2.rowcount == 1:

            flash('You already submitted a review for this book', 'warning')
            return redirect("/book/" + isbn)

        # Convert to save into DB
        rating = int(rating)

        db.execute("INSERT INTO reviews (user_id, book_id, description, rating) VALUES \
                    (:user_id, :book_id, :description, :rating)",
                    {"user_id": currentUser,
                    "book_id": bookId,
                    "description": description,
                    "rating": rating})

        # Commit transactions to DB and close the connection
        db.commit()

        flash('Review submitted!', 'info')

        return redirect("/book/" + isbn)

    # Take the book ISBN and redirect to his page (GET)
    else:

        row = db.execute("SELECT isbn, title, author, year FROM books WHERE \
                        isbn = :isbn",
                        {"isbn": isbn})

        bookInfo = row.fetchall()

        """ GOODREADS reviews """

        # Read API key from env variable
        key = os.getenv("GOODREADS_KEY")

        # Query the api with key and ISBN as parameters
        query = requests.get("https://www.goodreads.com/book/review_counts.json", # rever este link em https://www.goodreads.com/api/index
                params={"key": key, "isbn": isbn})

        # Convert the response to JSON
        response = query.json()

        # "Clean" the JSON before passing it to the bookInfo list
        response = response['books'][0]

        # Append it as the second element on the list. [1]
        bookInfo.append(response)

        """ Users reviews """

         # Search book_id by ISBN
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
                        {"isbn": isbn})

        # Save id into variable
        book = row.fetchone() # (id,)
        book = book[0]

        # Fetch book reviews
        # Date formatting (https://www.postgresql.org/docs/9.1/functions-formatting.html)
        results = db.execute("SELECT users.username, comment, rating, \
                            to_char(time, 'DD Mon YY - HH24:MI:SS') as time \
                            FROM users \
                            INNER JOIN reviews \
                            ON users.id = reviews.user_id \
                            WHERE book_id = :book \
                            ORDER BY time",
                            {"book": book})

        reviews = results.fetchall()

        return render_template("book.html", bookInfo=bookInfo, reviews=reviews)


@app.route("/api/<isbn>", methods=['GET'])
@login_required
def api_call(isbn):

    # COUNT returns rowcount
    # SUM returns sum selected cells' values
    # INNER JOIN associates books with reviews tables

    row = db.execute("SELECT title, author, year, isbn, \
                    COUNT(reviews.id) as review_count, \
                    AVG(reviews.rating) as average_score \
                    FROM books \
                    INNER JOIN reviews \
                    ON books.id = reviews.book_id \
                    WHERE isbn = :isbn \
                    GROUP BY title, author, year, isbn",
                    {"isbn": isbn})

    # Error checking
    if row.rowcount != 1:
        return jsonify({"Error": "Invalid book ISBN"}), 422

    # Fetch result from RowProxy
    tmp = row.fetchone()

    # Convert to dict
    result = dict(tmp.items())

    # Round Avg Score to 2 decimal. This returns a string which does not meet the requirement.
    # https://floating-point-gui.de/languages/python/
    result['average_score'] = float('%.2f'%(result['average_score']))

    return jsonify(result)
