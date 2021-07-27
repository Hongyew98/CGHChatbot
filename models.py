from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy, model
from flask_migrate import Migrate

#To edit db schema
#migrate = Migrate(app, db)
app = Flask(__name__)
app.config["SECRET_KEY"] = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Applicants(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #unique ID
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    job = db.Column(db.String(100), nullable=False)
    #cv = db.Column(db.LargeBinary)
    score = db.Column(db.Integer)
    status = db.Column(db.String)
    comments = db.Column(db.String)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String)
    status = db.Column(db.String)
    answer = db.Column(db.String)

if __name__ == "__main__":
    db.create_all()