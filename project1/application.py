import os, requests

from database import *
from flask import Flask, session,render_template, request,redirect,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
   raise RuntimeError("DATABASE_URL is not set")

app.config['SQLALCHEMY_DATABASE_URI'] =os.getenv("DATABASE_URL")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASE_URL.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure session to use filesystem      
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db.init_app(app)
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
Session = scoped_session(sessionmaker(bind=engine))
DB = Session()
# session=Session() ++-*/9+ 
@app.route("/")
def index():
    name = session.get('name')
    if session.get('mail') is None:
        return render_template("registerForm.html")
    return render_template("Home.html", name=name)
@app.route("/register", methods = ['POST', 'GET'])
def register():
    name = session.get('name')
    print(name)
    if session.get('mail') is None:
        if request.method =='POST':
            data=user(request.form['name'],request.form['password'],request.form['mail'],
            request.form['gender'],request.form['age'],request.form['birthday'])
            userdata=user.query.filter_by(mail=request.form['mail']).first()
            if userdata is not None:
                return render_template("registerForm.html", message="Error!!Email_Id already exists")
            db.session.add(data)
            db.session.commit()
            print("Sucesssfully Registered")
            return render_template("registerForm.html", message="Sucesssfully Registered")
        else:
            return render_template("registerForm.html")
    return render_template("Home.html", name=name)

@app.route('/admins')
def admin():
    users = user.query.all()
    return render_template("Details.html",register = users)

@app.route('/auth',methods=['POST','GET'])
def auth():
    if request.method =='POST':
        name = request.form.get("name")
        email = request.form.get("mail")
        pwd = request.form.get("password")
        details = user.query.get(email)
        if details != None:
            if pwd == details.password:
                session['mail'] = email
                session['name'] = name
                return render_template("Home.html", name=name)
            else:
                return "Wrong password!!"
        else:
            return render_template("registerForm.html", message = "Register to login")
            
@app.route('/logout', methods=['POST','GET'])
def logout():
    session['mail'] = None
    return redirect('/register')
# @app.route("/book/<string:isbn>")
# def book(isbn):
#     booksdata = db.session.query(Book).filter(Book.isbn == isbn)
#     return redirect("/review")
@app.route("/review/<string:arg>",methods=['POST','GET'])
def rev(arg):
    if session.get("mail") is None:
        return redirect("/register")
    isbn = arg.strip().split("=")[1]
    #booksdata = db.session.query(Book).filter(Book.isbn == isbn).first()
    book = db.session.query(Book).filter_by(isbn = isbn).first()
    feedback = db.session.query(review).filter_by(title=book.title).all()
    name=session.get('name')
    print(name)
    if request.method=='POST':
        title = book.title
        rating=request.form.get("rating")
        feedback1=request.form.get("feedback")
        Rdata=review(name,title,rating,feedback1)
        try:
            db.session.add(Rdata)
            db.session.commit()
            feedback=db.session.query(review).filter_by(title=book.title).all()
            r=review.query.filter_by(title=book.title).all()
            return render_template("review.html",data=book,name=name,feedback=feedback,message="Thank you!! for the feedback")
        except:
            db.session.rollback()
            return render_template("review.html",data=book,name=name,feedback=feedback,message="user has already given review")
    else :              
        return render_template("review.html",data=book,name=name,feedback=feedback)
@app.route("/api/Sreview", methods  =['POST'])
def submitreview():
    if not request.is_json:
        message = "Invalid request format"
        return jsonify(message),400
    isbn = request.args.get('isbn')
    try:
        book = db.session.query(Book).filter(isbn == isbn).first()
    except:
        message = "Please Try again Later"
        return jsonify(message),500
    if book is None:
        message = "Please enter valid ISBN"
        return jsonify(message), 404
    userName = session.get('name')
    title = "At Grave's End"
    rating = request.get_json()['rating']
    feedback = request.get_json()['feedback']
    user = review.query.filter_by(userName=userName,title=book.title).first()
    if user is not None:
        message = "Sorry you can't review this book again"
        print(message)
        return jsonify(message), 409
    reviewdata=review(userName,title,rating,feedback)
    try:
        db.session.add(reviewdata)
        db.session.commit()
    except:
        message = "Please Try Again "
        return jsonify(message), 500
    # print(isbn,rating,comment)
    message = "Review submitted successfully"
    return jsonify(message), 200

@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == "POST":
        name = session.get('name')
        searchType = request.form.get("searchType")
        search = request.form.get("search")   
        book = []
        message = ""
        matchString = "%{}%".format(search)
        print(matchString)
        if searchType == 'isbn':
            book = db.session.query(Book).filter(Book.isbn.like(matchString)).all()
        elif searchType == 'title':
            book = db.session.query(Book).filter(Book.title.like(matchString)).all()
        elif searchType == 'author':
            book = db.session.query(Book).filter(Book.author.like(matchString)).all()
        if len(book)== 0:
            message = "No Matching results found!"
        print (book)
        return render_template("Home.html", name=name, books = book, message = message)

    return render_template("Home.html", name=name)