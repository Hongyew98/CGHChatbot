import os
import secrets
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from flask import current_app
from ..forms import *
from ..models import *
from urllib.parse import quote, unquote

hr = Blueprint("hr", __name__, static_folder="static", static_url_path="/hr/static", template_folder="templates")

@hr.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("bot.chatbot"))

@hr.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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

@hr.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
       return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if form.email.data=="admin@cgh.com":
            flash("Login successful!", "success")
            return redirect(url_for("hr.overview"))
        elif user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("temporary.submit"))
        else:
            flash("Invalid login details. Please try again.", "danger")
    return render_template("login.html", form=form)

@hr.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("temporary.login"))

def save_cv(form_cv):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_cv.filename) #_ is to throw away variable name
    cv_fn = random_hex + f_ext
    cv_path = os.path.join(hr.root_path, "static/CVs", cv_fn)
    form_cv.save(cv_path)
    return cv_fn

@hr.route("/account", methods=["GET", "POST"])
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
        redirect(url_for("temporary.account"))
    elif request.method == "GET":
        form.cv.data = current_user.cv
    cv = url_for("static", filename="CVs/" + current_user.cv)
    return render_template("account.html", cv=cv, form=form)