import os, csv

from flask import Flask, render_template, request
from database import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")  
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

    with open("books.csv", 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            newBook = Book(row[0], row[1], row[2], int(row[3]))
            db.session.add(newBook)
    db.session.commit()

if __name__ == "__main__":      
    with app.app_context():
        main()