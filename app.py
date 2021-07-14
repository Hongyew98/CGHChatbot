from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import Applicants

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return redirect("/login")
    else:
        if str(request.form.get("email")) != 'admin':
            return 'Invalid login'
        else:
            return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return redirect("/login")

@app.route("/applicants")
def applicants():
    return render_template("applicants.html", applicants=Applicants.query.all())

@app.route("/id<int:appid>")
def applicant(appid):
    applicant = Applicants.query.filter_by(id=appid).first()
    if appid == applicant.id:
        return render_template("applicant.html", applicant=applicant)
    else:
        return "try again"

#@app.route("/questions")
#def questions():
#    return "questions"

#@app.route("/processed")
#def processed():
#    return "processed"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)