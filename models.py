from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#To edit db schema
#migrate = Migrate(app, db)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Applicants(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #unique ID
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    job = db.Column(db.String(100), nullable=False)
    #cv = db.relationship()
    score = db.Column(db.Integer)
    status = db.Column(db.String)
    comments = db.Column(db.String)