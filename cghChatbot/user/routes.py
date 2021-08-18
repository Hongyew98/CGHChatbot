from flask import Blueprint, render_template, request
from ..chatbot import processor

user = Blueprint("user", __name__, static_folder="static", template_folder="templates")

@user.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@user.route("/quiz", methods=["GET", "POST"])
def quiz():
    return render_template("quiz.html")