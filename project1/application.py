import os, requests

from database import *
from flask import Flask, session,render_template, request,redirect
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
            book = DB.query(Book).filter(Book.isbn.like(matchString)).all()
        elif searchType == 'title':
            book = DB.query(Book).filter(Book.title.like(matchString)).all()
        elif searchType == 'author':
            book = DB.query(Book).filter(Book.author.like(matchString)).all()
        if len(book)== 0:
            message = "No Matching results found!"
        print (book)
        return render_template("Home.html", name=name, books = book, message = message)

    return render_template("Home.html", name=name)


@app.route("/book/<string:arg>")
def book(arg):
    return render_template("Book.html", isbn = arg)
