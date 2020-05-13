import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Book(db.Model):
    __tablename__="books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    review = db.relationship("Review", backref="book", lazy=True)

    def add_review(self, id, rating, description):
        bookreview = Review(id=id, rating=rating, description=description, book_id=self.id)
        db.session.add(bookreview)
        db.session.commit ()

class Review(db.Model):
    __tablename__="reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    #authenticated = db.Column(db.Boolean, default=False)

#    def__init__(self, username, password):
#        self.username = username
#        self.password = Password
        #self.authenticated = datetime.utcnow()

#        db.Model.metadata,create_all(engine)

#    def is_authenticated(self):
#        return True

#    def is_active(self):
#        return True

#    def is_anonymous(self):
#        return False

#    def get_id(self):
#        return unicode(self.id)

#    def __repr__(self):
#        return '<User %r>' % (self.username)


# @validates('firstname', 'lastname')
#    def convert_capitalize(self, key, value):
#        return value.capitalize()
