import json
from flask import Blueprint, render_template, request, url_for
from flask_login import current_user
from urllib.parse import quote, unquote
from .processor import *

bot = Blueprint("bot", __name__, url_prefix="/chatbot", static_folder="static", static_url_path="/CGHChatbot/cghChatbot/chatbot", template_folder="templates")

@bot.route("/")
def chatbot():
    if current_user.is_authenticated:
        image = url_for("user.static", filename="profile_pics/" + current_user.image)
    else:
        image = url_for("user.static", filename='profile_pics/default.png')
    return render_template("chatbot.html", image=image)

@bot.route("/new")
def chatnew():
    # job=unquote(jobquote)
    if current_user.is_authenticated:
        image = url_for("user.static", filename="profile_pics/" + current_user.image)
        logged = True
    else:
        image = url_for("user.static", filename='profile_pics/default.png')
        logged = False
    return render_template("chatbot_copy.html", image=image, logged=logged)


@bot.route("/send", methods=["GET", "POST"])
def send():
    question = request.args.get("msg")
    return chatbot_response(question)

@bot.route("/next", methods=["GET", "POST"])
def next():
    answer = ["hello","look in chatbot/routes.py"]
    return json.dumps(answer)

@bot.route("/answer", methods=["GET", "POST"])
def answer():
    answer = ["answer1","answer2","answer3"]
    return json.dumps(answer)