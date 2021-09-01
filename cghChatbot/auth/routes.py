from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from ..models import *
from .forms import *
from .utils import *

auth = Blueprint("auth", __name__, static_folder="static", static_url_path="/CGHChatbot/cghChatbot/auth", template_folder="templates")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("admin.index")) if current_user.admin() else redirect(url_for("user.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        db.session.add(User(firstname=form.firstname.data,
                            lastname=form.lastname.data,
                            email=form.email.data,
                            password=generate_password_hash(form.password.data, method='sha256')))
        db.session.commit()
        flash("Account successfully created!", "success")
        return redirect(url_for("auth.login"))
    return render_template("signup.html", title="Sign Up", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.index")) if current_user.admin() else redirect(url_for("user.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("admin.index")) if user.admin() else redirect(url_for("user.index"))
        else:
            flash("Invalid login. Please try again.", "danger")
    return render_template("login.html", title="Login", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth.route("/resetpassword", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
       return redirect(url_for("admin.index")) if current_user.admin() else redirect(url_for("user.index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("auth.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@auth.route("/resetpassword/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
       return redirect(url_for("admin.index")) if current_user.admin() else redirect(url_for("user.index"))
    user = User.verify_reset_token(token)
    if not user:
        flash("That token is invalid or expired.", "warning")
        return redirect(url_for("auth.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password=generate_password_hash(form.password.data, method='sha256')
        db.session.commit()
        flash("Your password has been updated.", "success")
        return redirect(url_for("auth.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)