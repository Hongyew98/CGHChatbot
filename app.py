from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import Applicants, Questions

app = Flask(__name__)
app.config["SECRET_KEY"] = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return redirect("/login")
    else:
        if str(request.form.get("email")) != 'admin@cgh.com' or str(request.form.get("password")) != 'test':
            flash('Invalid login.')
            return redirect("/login")
        else:
            return redirect("/main")

@app.route("/main")
def main():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return redirect("/login")

@app.route("/newlisting", methods=["GET", "POST"])
def newlisting():
    return render_template("newlisting.html")

@app.route("/applicants", methods=["GET", "POST"])
def applicants():
    sort = ""
    if request.method == "POST":
        sort = request.form.get("sort")
    return render_template("applicants.html", applicants=Applicants.query.all(), sort=sort)

@app.route("/id<int:appid>", methods=["GET", "POST"])
def applicant(appid):
    applicant = Applicants.query.filter_by(id=appid).first()
    if request.method == "POST":
        comments = request.form.get("comments")
        applicant.comments = comments        
        status = request.form.get("status")
        if status:
            applicant.status = status
            flash(f"Applicant ID {appid} {status}.", "info")
        current_db_session = db.session.object_session(applicant)
        current_db_session.add(applicant)
        current_db_session.commit()
        #applicant = Applicants.query.filter_by(id=appid).first()
    if appid == applicant.id:
        return render_template("applicant.html", applicant=applicant)
    else:
        return "invalid id"

@app.route("/questions", methods=["GET", "POST"])
def questions():
    if request.method == "POST":
        id = request.form.get("id")
        answer = request.form.get("answer")
        question  = Questions.query.filter_by(id=id).first()
        question.answer = answer
        if answer:
            question.status = "Resolved"
        else:
            question.status = "Pending"
        current_db_session = db.session.object_session(question)
        current_db_session.add(question)
        current_db_session.commit()
    return render_template("questions.html", questions=Questions.query.all())

@app.route("/completed")
def completed():
    return render_template("completed.html", applicants=Applicants.query.all())

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)