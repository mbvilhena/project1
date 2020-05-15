import os

from flask import Flask, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
from sqlalchemy.orm import validates
from functools import wraps
from wtforms import Form, BooleanField, StringField, PasswordField, validators

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
#    review = db.relationship("Review", backref="book", lazy=True)

#    def add_review(self, id, rating, description):
#        """ Add review to Book """
#        bookreview = Review(id=id, rating=rating, description=description, book_id=self.id)
#        db.session.add(bookreview)
#        db.session.commit ()

# Review class
class Review(db.Model):
    """ Review """
    __tablename__="reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#    time = db.Column(db.Timestamp, nullable=False)

# User class
class User(db.Model):
    """ User """
    __tablename__="users"
    id = db.Column(db.Integer, Sequence("id_seq"), primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String, nullable=False)

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

    username = StringField('username', [validators.Length(min=4, max=25)])
    name = StringField('name', [validators.Length(min=6, max=35)])

    # Confirm Password
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

    # Confirm Submission
    accept_tos = BooleanField('Confirm', [validators.DataRequired()])
