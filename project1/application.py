import os

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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure session to use filesystem      
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db.init_app(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
Session = scoped_session(sessionmaker(bind=engine))
session=Session()
@app.route("/")
def index():
    return "project 1:TODO"
@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method =='POST':
        udata=user(request.form['name'],request.form['password'],request.form['mail'],
        request.form['gender'],request.form['age'],request.form['birthday'])
        userd=user.query.filter_by(mail=request.form['mail']).first()
        if userd is not None:
            return render_template("error.html")
        db.session.add(udata)
        db.session.commit()
        print("Sucesssfully Registered")
        return render_template("sucess.html")
    else:
        return render_template("registerForm.html")

@app.route('/admins')
def admin():
    usersinfo = user.query.all()
    return render_template("Details.html",register = usersinfo)







