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
#app.config["SECRET KEY"] = ""
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

###
@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("") is None:
        session[""] =
    if session.method == "POST":


###

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("users") is None:
        session["users"] = []
    if request.method == "POST":
        user = request.form.get ("user")
        session["users"].append(user)
    return render_template("index.html", users=session["user"])

    if request.method == "POST":
        req = request.form

        username = req.get("username")
        password = req.get("password")

        if not username in users:
            print("Username not found")
            return redirect(request.url)
        else:
            user = users[username]
        if not password == user["password"]:
            print("Incorrect password")
            return redirect(request.url)
        else:
            session["USERNAME"] = ["username"]
            print("Welcome {"username"}")
            return redirect(url for profile)
    return render_template("/html page ")


@app.route("/booklist")
def booklist():
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("dashboard.html", books=books)



###
@app.route("/register", methods=["GET", "POST"])

def register():
    if request.method == "GET"
        return render_template("register.html")
    user = User(request.form["username"], request.form["firstname"], request.form["lastname"], request.form ["password"])
    db.session.add(user)
    db.session.commit()
    flash("User sucessfully registered")
    return redirect("/login")


@app.route("login", methods=["GET", "POST"])

def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    password = request.form["password"]

    register_user = User.query.filter_by(username=username,password=password).first()
                    #raw SQL with db.execute

    if register_user is None:
        flash("Username or Password is invalid", "error")
        #verify with harvard standarts
        return redirect ("/login")

    login_user(register_user)
    flash ("Logged in successfully")
    return redirect(request.args.get('next') or url_for('index'))


@app.route("/logout")

def logout():
    session.clear()
    logout.user()
    return redirect ("/index")


#https://www.openshift.com/blog/use-flask-login-to-add-user-authentication-to-your-python-application
#build html pages and insert {{}}
#review all sintax according to harvard classes



@app.route("/dashboard", methods=["GET"])
def dashboard():
    for book in books:
        print(book)
    return render_template("dashboard.html", books=books)



@app.route("/user", methods=["GET"])
def user():
    for review in reviews:
        print(reviews)
    return render_template("user.html", reviews=session["reviews"])














#def main():
#    res = requests.get("https://www.goodreads.com/book/review_counts.json",
#        params={"key": "CoB12efyXvsy5aQaD9BLw", "isbns": "9781632168146"})
#    print(res.json())

#if __name__ == "__main__":
#    main()





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

        elif not request.form.get("name"):
            flash("Name missing")

        hashed_password = generate_password_hash(request.form.get("password"), method="sha256")

        db.execute("INSERT INTO users (username, name, password) VALUES (:username, :name, :password)", {"username":request.form.get("username"), "name":request.form.get("name"), "password":hashed_password})

        db.commit()

        flash("Account created, please login")

        return render_template("login.html")

    else:
        return render_template("register.html")
