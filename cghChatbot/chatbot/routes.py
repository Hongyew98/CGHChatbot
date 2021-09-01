from flask import Blueprint, render_template, request, url_for
from flask_login import current_user
from .processor import *

bot = Blueprint("bot", __name__, url_prefix="/chatbot", static_folder="static", static_url_path="/CGHChatbot/cghChatbot/chatbot", template_folder="templates")

@bot.route("/")
def chatbot():
    if current_user.is_authenticated:
        image = url_for("user.static", filename="profile_pics/" + current_user.image)
    else:
        image = url_for("user.static", filename='profile_pics/default.png')
    return render_template("chatbot.html", image=image)

@bot.route("/send", methods=["GET", "POST"])
def send():
    question = request.args.get("msg")
    return chatbot_response(question)