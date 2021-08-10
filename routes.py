import os
import secrets
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from . import app
from .forms import *
from .models import *
from urllib.parse import quote, unquote


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/overview", methods=["GET", "POST"])
def overview():
    search=request.form.get("search")
    if search:
        job = Job.query.filter_by(title=search).first()
        if job:
            jobs = [job]
        else:
            flash("Job not found", "info")
            jobs = Job.query.all()
    else:
        jobs = Job.query.all()
    applications=[]
    for job in jobs:
        application=[]
        application.append(job.title)
        application.append(Application.query.filter_by(job=job.title).count())
        application.append(Application.query.filter_by(job=job.title, status="Awaiting Interview").count())
        application.append(Application.query.filter_by(job=job.title, status="Reviewed").count())
        applications.append(application)

    return render_template("overview.html", applications=applications)

@app.route("/alljobs")
def alljobs():
    page = request.args.get("page", 1, type=int)
    job = Job.query.order_by(Job.date_created.desc()).paginate(page=page, per_page=8)
    return render_template("alljobs.html", job=job)

@app.route("/job/new", methods=["GET", "POST"])
def newjob():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, description=form.description.data, type=form.type.data, minpay=form.minpay.data, maxpay=form.maxpay.data)
        db.session.add(job)
        db.session.commit()
        flash("Job listing created", "success")
        return redirect(url_for("newjob"))
    return render_template("newjob.html", legend="New Job", form=form)

@app.route("/job/<string:titlequote>")
def job(titlequote):
    title=unquote(titlequote)
    job = Job.query.filter_by(title=title).first()
    return render_template("job.html", job=job)

@app.route("/job/<string:titlequote>/edit", methods=["GET", "POST"])
def editjob(titlequote):
    title=unquote(titlequote)
    job = Job.query.filter_by(title=title).first()
    form = JobForm()
    form.title.data=job.title
    form.description.data=job.description
    form.type.data=job.type
    form.minpay.data=job.minpay
    form.maxpay.data=job.maxpay
    if form.validate_on_submit():
        job.title=form.title.data
        job.description=form.description.data
        job.type=form.type.data
        job.minpay=form.minpay.data
        job.maxpay=form.maxpay.data
        db.session.commit()
        flash("Job listing edited", "success")
        return redirect(url_for("job", titlequote=quote(job.title)))
    return render_template("newjob.html", legend="Edit Job", form=form)

@app.route("/job/<string:titlequote>/delete", methods=["POST"])
def deletejob(titlequote):
    title=unquote(titlequote)
    job = Job.query.filter_by(title=title).first()
    db.session.delete(job)
    db.session.commit()
    flash("Job listing deleted", "success")
    return redirect(url_for("alljobs"))

@app.route("/<string:titlequote>/applicants", methods=["GET", "POST"])
@app.route("/applicants", methods=["GET", "POST"])
def applicants(titlequote=""):
    title=unquote(titlequote)
    page = request.args.get("page", 1, type=int)
    sort = request.form.get("sort")
    if not title and (sort=="All" or not sort):
        applicants=Application.query.order_by(Application.date_applied.desc()).paginate(page=page, per_page=10)
    elif not title and sort:
        applicants=Application.query.filter_by(status=sort).order_by(Application.date_applied.desc()).paginate(page=page, per_page=10)
    elif title and (sort=="All" or not sort):
        applicants=Application.query.filter_by(job=title).order_by(Application.date_applied.desc()).paginate(page=page, per_page=10)
    elif title and sort:
        applicants=Application.query.filter_by(job=title, status=sort).order_by(Application.date_applied.desc()).paginate(page=page, per_page=10)
    return render_template("applicants.html", applicants=applicants, title=title, sort=sort)

@app.route("/applicant/<int:appid>", methods=["GET", "POST"])
def applicant(appid):
    application = Application.query.get(appid)
    if request.method == "POST":
        comments = request.form.get("comments")
        application.comments = comments        
        status = request.form.get("status")
        if status:
            application.status = status
            flash(f"Applicant ID {appid} {status}.", "info")
        db.session.commit()
    return render_template("applicant.html", application=application)

@app.route("/completed")
def completed():
    return render_template("completed.html", applicant=Application.query.filter_by(status="Completed").first())

@app.route("/questions", methods=["GET", "POST"])
def questions():
    if request.method == "POST":
        id = request.form.get("id")
        answer = request.form.get("answer")
        question  = Question.query.filter_by(id=id).first()
        question.answer = answer
        if answer:
            question.status = "Resolved"
        else:
            question.status = "Pending"
        db.session.commit()
        # current_db_session = db.session.object_session(question)
        # current_db_session.add(question)
        # current_db_session.commit()
    return render_template("questions.html", questions=Question.query.all())

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")






@app.route("/quiz")
def quiz():
    return render_template("quiz.html")







@app.route("/submit", methods=["GET", "POST"])
def submit():
    job = Job.query.all()
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        if firstname:
            email = request.form.get("email")
            password = "test"
            # cv = request.files("cv")
            # cv.save(cv.filename)
            db.session.add(User(firstname=firstname, lastname=lastname, email=email, password=password))
            job = request.form.get("job")
            score = request.form.get("score")
            db.session.commit()
            user_id = User.query.filter_by(firstname=firstname).first()
            db.session.add(Application(job=job, score=score, user_id=user_id.id))
            db.session.commit()
            flash(f"{firstname} successfully applied!", "info")
        question = request.form.get("question")
        if question:
            email = request.form.get("email")
            db.session.add(Question(email=email, question=question))
            db.session.commit()
            flash(f"{firstname}'s question asked!", "info")
    return render_template("submit.html", job=job)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("submit"))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            form.email.errors="This email is already taken"
        else:
            db.session.add(User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=generate_password_hash(form.password.data, method='sha256')))
            db.session.commit()
            flash("Account successfully created!", "success")
            return redirect(url_for("login"))
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
#    if current_user.is_authenticated:
#        return redirect(url_for(""))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if form.email.data=="admin@cgh.com":
            flash("Login successful!", "success")
            return redirect(url_for("overview"))
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

def save_cv(form_cv):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_cv.filename) #_ is to throw away variable name
    cv_fn = random_hex + f_ext
    cv_path = os.path.join(app.root_path, "static/CVs", cv_fn)
    form_cv.save(cv_path)
    return cv_fn

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.cv.data:
            cv_file = save_cv(form.cv.data)
            current_user.cv = cv_file
        current_user.cv = form.cv.data
        db.session.commit()
        flash("CV uploaded successfully!", "success")
        redirect(url_for("account"))
    elif request.method == "GET":
        form.cv.data = current_user.cv
    cv = url_for("static", filename="CVs/" + current_user.cv)
    return render_template("account.html", cv=cv, form=form)