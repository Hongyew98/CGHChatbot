from flask import Flask, render_template, request, redirect
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///applicants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
ADMIN = {'admin@admin.com'}

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return redirect("/login")
    else:
        if str(request.form.get("email")) != 'admin@admin.com':
            return 'Invalid login'
        else:
            return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

#@app.route("/logout")
#def logout():
#    return redirect("/login")

#@app.route("/applicants")
#def applicants():
#    return "applicants"

#@app.route("/applicant")
#def applicants():
#    return "applicant"

#@app.route("/questions")
#def applicants():
#    return "questions"

#@app.route("/processed")
#def processed():
#    return "processed"

if __name__ == "__main__":
    app.run(debug=True)