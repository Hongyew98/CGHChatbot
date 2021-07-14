from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from models import Applicants

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        job = request.form.get("job")
        score = request.form.get("score")
        db.session.add(Applicants(name=name, email=email, job=job, score=score, status="Processing"))
        db.session.commit()
        flash(f"{name} successfully applied!", "info")
    return render_template("submit.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)