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