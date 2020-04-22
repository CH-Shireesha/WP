from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class user(db.Model):
    __tablename__ = "user_details"
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False, primary_key=True)
    gender = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    birthday = db.Column(db.DATE, nullable=False) 

    def __init__(self,name,password,mail,gender,age,birthday):
        self.name=name
        self.password=password
        self.mail=mail
        self.gender=gender
        self.age=age
        self.birthday=birthday


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(80), index=False, unique=True, nullable=False)
    title = db.Column(db.String(80), index=True, unique=False, nullable=False)
    author = db.Column(db.String(128))
    year = db.Column(db.Integer, index=False, unique=False, nullable=False)

    def __init__(self, isbn, title, author, year) :
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self):
        return self.title
