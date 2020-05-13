import os
import requests
import json

from flask import Flask, session, render_template, request, jsonify, url_for, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from werkzeug.security import generate_password_hash, check_password_hash

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


@app.route("/")
def index():
    """ Index Page """
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register User """
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            flash("Username missing")

        check_user = db.execute("SELECT * FROM users WHERE username = :username", {"username":request.form.get("username")}).fetchone()

        if check_user:
            flash("Username already exists")

        elif not request.form.get("password"):
            flash("Password missing")

#        elif not request.form.get("confirmation"):
#            flash("Confirm password")

#        elif not request.form.get("password") == request.form.get("confirmation"):
#            flash("Passwords don't match")

        hashed_password = generate_password_hash(request.form.get("password"), method="sha256")

        db.execute("INSERT INTO users (username, name, password) VALUES (:username, :name, :password)", {"username":request.form.get("username"), "name":request.form.get("name"), "password":hashed_password})

        db.commit()

        flash("Account created, please login")

        return render_template("login.html")

    else:
        return render_template("register.html")


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

        session["id"] = result [0]
        session["username"] = result [1]

        return render_template("dashboard.html")

    else:
        return render_template("login.html")


#        username = request.form.get("username")
#        password = request.form.get("password")

#        if not username in users:
#            flash("username not found")
#            return redirect(url_for("login"))
#        else:
#            user = users.username
#        if not password == user["password"]:
#            flash("Incorrect password")
#            return redirect(url_for("login"))
#        else:
#            session["username"] = ["username"]
#            flash("Welcome {{username}}")
#            return redirect(url_for("login"))
#    return render_template("login.html")


#        if request.form["username"] in session ["username"] and request.form["password"] in session["password"]:
#            username = session["username"]
#            flash("Welcome {username}")
#            return render_template("dashboard.html", username=username)
#        flash("Incorrect password")
#    return redirect ("/")
#return render_template("login.html")


@app.route("/logout")
def logout():
    """ Logout User """

    session.clear()
    return redirect("/")


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """ List of all books """
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("dashboard.html", books=session["books"])


#####################################################

#search books --- AMANHÃ
@app.route("/search", methods=["GET", "POST"])
def search():
    if 'username' in session:
        if request.method == "POST":
            try:
                book_search = request.form.get("search")
                if not book_search:
                    return "please type a book name!"

                books = db.execute("SELECT * FROM books WHERE title LIKE :book_search OR isbn LIKE :book_search OR author LIKE :book_search", {"book_search": '%'+book_search+'%'}).fetchall()

                return render_template("search_result.html", books=books)

            except ValueError:
                return render_template("error.html", message="Please type a valid entry")

        return render_template("search.html")
    return render_template("not_logged_in.html")


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
