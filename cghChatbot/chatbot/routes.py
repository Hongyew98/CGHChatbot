from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from . import processor

bot = Blueprint("bot", __name__)

@bot.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@bot.route("/chatbot/send", methods=["GET", "POST"])
def send():
    question = request.args.get("msg")
    return processor.chatbot_response(question)
    # question = request.form.get('msg')
    # response = processor.chatbot_response(question)

    # return jsonify({"response": response })