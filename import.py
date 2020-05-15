import csv
import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    f = open("books.csv")
    reader = csv.reader(f)
    next(reader) #csvreader.__next__() - Return the next row of the reader’s iterable object as a list
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book with ISBN {isbn}, Title: {title}, from Author: {author}, Year {year}")
        db.commit()

if __name__ == "__main__":
    main()
