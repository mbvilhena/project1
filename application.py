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
@app.route('/register', methods=['GET', 'POST'])
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

        flash("Welcome {{user_name}}")
        # Redirect user to dashboard page
        return render_template("profile.html")

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
@app.route("/dashboard")
@login_required
def dashboard():
    pass
    """ List of all books """
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("dashboard.html", books=books)


# Book info
@app.route("/books/<int:book_isbn")
@login_required
def abook(book_isbn):
    """ Book details """

    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn}).fetchone()
    if book is None:
        flash("There is no such book.")
        return render_template("dashboard")

    # Get all books.
    books = db.execute("SELECT title FROM books WHERE book_isbn = :book_isbn",
                            {"book_isbn": book_isbn}).fetchall()
    return render_template("book.html", book=book)


# Set search bar
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    pass
    """ Search for books """
    if request.method == "POST":
        try:
            book_search = request.form.get("book_search")
            book_list = db.execute("SELECT * FROM books WHERE title LIKE :book_search OR isbn LIKE :book_search OR author LIKE :book_search", {"book_search": '%'+book_search+'%'}).fetchall()
            if not book_list:
                flash("please type a book name!")
                return render_template("dashboard.html")
            return render_template("book.html", books=books)
        except ValueError:
            flash("Please type a valid entry")
            return redirect("/search")
        return render_template("dashboard.html")

### API src4/Currency - book/<book>

@app.route("/user", methods=["GET"])
@login_required
def user_profile():
    pass
    """ Profile page """
    if request.method == "POST":
        user_name = session["user_name"]
        return render_template("profile.html", user_name=session["user_name"])
    else:
        return redirect("/login")

### to search books
#@app.route("/book", methods=["POST"])
#def book():
#    """Book a flight."""

#    # Get form information.
#    name = request.form.get("name")
#    try:
#        flight_id = int(request.form.get("flight_id"))
#    except ValueError:
#        return render_template("error.html", message="Invalid flight number.")

    # Make sure flight exists.
#    if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
#        return render_template("error.html", message="No such flight with that id.")
#    db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
#            {"name": name, "flight_id": flight_id})
#    db.commit()
#    return render_template("success.html")


### Details about single book

#@app.route("/flights/<int:flight_id>")
#def flight(flight_id):
#    """List details about a single flight."""

    # Make sure flight exists.
#    flight = db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).fetchone()
#    if flight is None:
#        return render_template("error.html", message="No such flight.")

    # Get all passengers.
#    passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
#                            {"flight_id": flight_id}).fetchall()
#    return render_template("flight.html", flight=flight, passengers=passengers)
