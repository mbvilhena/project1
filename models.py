import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Book(db.Model):
    __tablename__="books"
    isbn = db.Column(db.Char, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    review = db.relationship("Review", backref="book", lazy=True)

    def add_review(self, rating, description):
        bookreview = Review(rating=rating, description=description, book_isbn=self.id)
        db.session.add(bookreview)
        db.session.commit ()

class Review(db.Model):
    __tablename__="reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer[1,5], nullable=False)
    description = db.Column(db.String, nullable=False)
    book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)

class User(db.Model):
    __tablename__="users"
    username = db.Column(db.Varchar, unique=True, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    password = db.Column(db.Varchar(20), nullable=False)


# @validates('firstname', 'lastname')
#    def convert_capitalize(self, key, value):
#        return value.capitalize()
