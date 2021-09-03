from cghChatbot.chatbot.routes import chatbot
from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash
from flask_login.utils import login_required, current_user
from ..models import *
from .forms import *

user = Blueprint("user", __name__, static_folder="static", static_url_path="/CGHChatbot/cghChatbot/user", template_folder="templates")

@user.route("/", methods=["GET", "POST"])
@login_required
def index():

    return redirect(url_for("bot.chatbot"))

    # form = CVForm()
    # if request.method == "POST" and form.validate_on_submit:
    #     if not current_user.is_authenticated:
    #         return current_app.login_manager.unauthorized()
    #     if form.cv.data:
    #         current_user.cvname = form.cv.data.filename
    #         cv = save_cv(form.cv.data)
    #         delete(current_user.cv)
    #         current_user.cv = cv
    # cvname = current_user.cvname if current_user.cv else ""
    # return render_template("index_user.html", title="Apply", form=form, cvname=cvname)

@user.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == "POST" and form.validate_on_submit():
        current_user.email = form.email.data
        if form.image.data:
            newImage = save_picture(form.image.data)
            if current_user.image != "default.png":
                delete(current_user.image)
            current_user.image = newImage
        if form.cv.data:
            current_user.cvname = form.cv.data.filename
            cv = save_cv(form.cv.data)
            delete(current_user.cv)
            current_user.cv = cv
        if form.password.data and form.new_password.data:
            current_user.password = generate_password_hash(form.password.data, method='sha256')
        db.session.commit()
        flash("Your account has been updated.", "info")
        return redirect(url_for("user.account"))
    elif request.form.get("button"):
        return redirect(url_for("user.quiz"))
    elif request.method == "GET":
        form.email.data = current_user.email
    image = url_for("user.static", filename="profile_pics/" + current_user.image)
    cvname = current_user.cvname if current_user.cv else ""
    return render_template("account.html", title="Account", image=image, form=form, cvname=cvname)

@user.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    return render_template("quiz.html")