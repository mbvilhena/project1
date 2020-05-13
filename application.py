import os
import requests

from flask import Flask, session, render_template, request, jsonify, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
import requests
import json
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#app.config["SECRET KEY"] = ""
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Index
@app.route("/")
def index():
    return render_template("index.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.get_json()
        hashed_password = generate_password_hash(user["password"], method="sha256")
        new_user = User(request.form["username"], request.form["name"], request.form ["password"])
        db.session.add(new_user)
        db.session.commit()
        flash("User sucessfully registered")
        return redirect(url_for("login"))
    else:
        return render_template("register.html")
        flash("User not registered")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username in users:
            flash("username not found")
            return redirect(url_for("login"))
        else:
            user = users.username
        if not password == user["password"]:
            flash("Incorrect password")
            return redirect(url_for("login"))
        else:
            session["username"] = ["username"]
            flash("Welcome {{username}}")
            return redirect(url_for("login"))
    return render_template("login.html")

#        if request.form["username"] in session ["username"] and request.form["password"] in session["password"]:
#            username = session["username"]
#            flash("Welcome {username}")
#            return render_template("dashboard.html", username=username)
#        flash("Incorrect password")
#    return redirect ("/")
#return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Dashboard
@app.route("/dashboard")
def dashboard():
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("dashboard.html", books=books)


### error with dashboard, acessible without login!!!

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
