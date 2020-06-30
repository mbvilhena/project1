import os

from flask import Flask, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from functools import wraps
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField

db = SQLAlchemy()


# Login Required Decorator (Flask’s documentation)
def login_required(f):
    """ Login Required Decorator """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# Tables created in create.sql
# List of all books in books.csv
# Books imported to DB through import.py

# Book and add Review to Book
class Book(db.Model):
    """ Book """
    __tablename__="books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)


# Review class
class Review(db.Model):
    """ Review """
    __tablename__="reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# User class
class User(db.Model):
    """ User """
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(35), nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.name}')"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    # Capitalize Name
    @validates("name")
    def convert_capitalize(self, key, value):
        return value.capitalize()


# Form Validation with WTForms (Flask’s documentation)
class RegistrationForm(Form):
    """ Registration Form for User """

    username = StringField("username", [validators.DataRequired(), validators.Length(min=4, max=20)])
    name = StringField("name", [validators.DataRequired(), validators.Length(min=6, max=35)])

    # Confirm Password
    password = PasswordField("password", [
        validators.DataRequired(),
        validators.EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm Password")

    # Confirm Submission
    submit = SubmitField("register")
