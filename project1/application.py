import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("registerForm.html")

@app.route("/Details", methods=["POST"])
def form():
    name = request.form.get("Username")
    mail = request.form.get("email_id")
    gender = request.form.get("gender")
    age = request.form.get("Age")
    Birthday = request.form.get("birthday")
    return render_template("Details.html", name=name, mail=mail, gender=gender, age=age, Birthday=Birthday)