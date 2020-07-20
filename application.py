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
        return render_template("index.html", user_name=session["user_name"])

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


@app.route("/book/<isbn>", methods=["GET", "POST"])
@login_required
def book(isbn):
    """ Each book's page with Goodreads Reviews and Rating Submission """

    if request.method == "GET":

        row = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn", {"isbn": isbn})

        book_info = row.fetchall()

        # Goodreads reviews
        key = os.getenv("GOODREADS_KEY")

        # API call: https://www.goodreads.com/api/index#book.review_counts
        review_query = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})

        if review_query.status_code == 422 or review_query.status_code == 404:
            raise Exception("ERROR: API request unsuccessful.")

        review_stats = review_query.json()["books"][0]

        book_info.append(review_stats)

        # Fetch user reviews
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn})
        book_id = row.fetchone()[0]

        # Fetch book reviews
        rows = db.execute("SELECT username, description, rating FROM users JOIN reviews ON users.id = reviews.user_id \
                    WHERE book_id = :book_id", {"book_id": book_id})

        reviews = rows.fetchall()

        return render_template("book.html", book_info=book_info, reviews=reviews)

    else:
        # if POST method
        current_user = session["user_id"]

        # Fetch data from the form in book.html
        rating = request.form.get("rating")
        description = request.form.get("description")

        row = db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn})
        book_id = row.fetchone()[0]

        check_row = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
                               {"user_id": current_user, "book_id": book_id})

        if check_row.rowcount == 1:
            flash("You already submitted a description for this book", "warning")
            return redirect("/book/" + isbn)

        # Save rating and review
        rating = int(rating)

        db.execute("INSERT INTO reviews (user_id, book_id, description, rating) VALUES (:user_id, :book_id, :description, :rating)",
                                 {"user_id": current_user, "book_id": book_id, "description": description, "rating": rating})
        db.commit()

        flash("Your review has been submitted.", "info")

        return redirect("/book/" + isbn)


@app.route("/api/<isbn>", methods=["GET"])
@login_required
def api_call(isbn):
    """ API Access """

    row = db.execute("SELECT title, author, year FROM books WHERE isbn = :isbn", {"isbn": isbn})
    result = dict(row.first())
    result["isbn"] = isbn

    review_counts_result = get_review_counts(isbn)

    result["average_score"] = review_counts_result["average_rating"]
    result["review_count"] = review_counts_result["number_ratings"]

    print(result)

    results_json = json.dumps(result, )

    return results_json
