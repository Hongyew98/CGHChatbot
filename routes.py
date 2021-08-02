from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from . import app
from .forms import RegistrationForm, LoginForm
from .models import *


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/overview", methods=["GET", "POST"])
def overview():
    return render_template("overview.html")

@app.route("/<int:job>/applicants", methods=["GET", "POST"])
def applicants(job):
    sort = ""
    if request.method == "POST":
        sort = request.form.get("sort")
    return render_template("applicants.html", applicants=Applications.query.all(), sort=sort)

@app.route("/id<int:appid>", methods=["GET", "POST"])
def applicant(appid):
    applicant = Applications.query.filter_by(id=appid).first()
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

@app.route("/completed")
def completed():
    return render_template("completed.html", applicants=Users.query.all())

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

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")




@app.route("/submitapp", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            email = request.form.get("email")
            job = request.form.get("job")
            #cv = request.files("cv")
            #cv.save(cv.filename)
            score = request.form.get("score")
            db.session.add(Applications(name=name, email=email, job=job, score=score, status="Processing", comments=""))
            db.session.commit()
            flash(f"{name} successfully applied!", "info")
        name = request.form.get("name2")
        if name:
            email = request.form.get("email2")
            question = request.form.get("question")
            db.session.add(Questions(name=name, email=email, question=question, status="Pending", answer=""))
            db.session.commit()
            flash(f"{name}'s question asked!", "info")
    return render_template("submit.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("submit"))
    form = RegistrationForm()
    if form.validate_on_submit():
        if Users.query.filter_by(email=form.email.data).first():
            form.email.errors="This email is already taken"
        else:
            db.session.add(Users(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=generate_password_hash(form.password.data, method='sha256')))
            db.session.commit()
            flash("Account successfully created!", "success")
            return redirect(url_for("login"))
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
@login_required
def login():
#    if current_user.is_authenticated:
#        return redirect(url_for(""))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if form.email.data=="admin@cgh.com":
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        elif user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("submit"))
        else:
            flash("Invalid login details. Please try again.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/account")
@login_required
def account():
    return render_template("account.html")