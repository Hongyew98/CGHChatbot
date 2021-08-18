from flask import Blueprint, render_template, request
from .processor import *

bot = Blueprint("bot", __name__, url_prefix="/chatbot", static_folder="static", static_url_path="/CGHChatbot/cghChatbot/chatbot", template_folder="templates")

@bot.route("/")
def chatbot():
    return render_template("chatbot.html")

@bot.route("/send", methods=["GET", "POST"])
def send():
    question = request.args.get("msg")
    return chatbot_response(question)