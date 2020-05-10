import os

from database import *
from flask import Flask, session,render_template, request,redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
session=db()

def bookdetail(arg):
    isbn=arg.strip().split(",")[1]
    data=session.query(Book).filter_by(isbn=isbn).first()
    if data is None:
        return "No book"
    return data