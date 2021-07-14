from enum import unique
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3' #mysql://root:helloworld!1@127.0.0.1:3306/CGH AI Chatbot'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Applicants(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #unique ID
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    job = db.Column(db.String(100), nullable=False)
    #cv = db.relationship()
    score = db.Column(db.Integer)
    complete = db.Column(db.Boolean)
    def __init__(self, email, name, job, score, complete):
        self.email = email
        self.name = name
        self.job = job
        self.score = score
        self.complete = complete

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(300), nullable=False)
    date = db.Column(db.Date, nullable=False)
    complete = db.Column(db.Boolean)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("apply.html", applicants_list=Applicants.query.all())

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    email = request.form.get("email")
    job = request.form.get("job")
    score = request.form.get("score")
    db.session.add(Applicants(name=name, email=email, job=job, score=score, complete=False))
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)