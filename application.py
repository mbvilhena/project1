import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import books, reviews, users

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
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("users") is None:
        session["users"] = []
    if request.method == "POST":
        user = request.form.get ("user")
        session["users"].append(user)
    return render_template("index.html", users=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect ("/")

@app.route("/booklist")
def booklist():
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("dashboard.html", books=books)






def main():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
        params={"key": "CoB12efyXvsy5aQaD9BLw", "isbns": "9781632168146"})
    print(res.json())

if __name__ == "__main__":
    main()
