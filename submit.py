from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from models import Applicants, Questions

app = Flask(__name__)
app.config["SECRET_KEY"] = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            email = request.form.get("email")
            job = request.form.get("job")
            #cv = request.files("cv")
            #cv.save(cv.filename)
            score = request.form.get("score")
            db.session.add(Applicants(name=name, email=email, job=job, score=score, status="Processing", comments=""))
            db.session.commit()
            flash(f"{name} successfully applied!", "info")
        name = request.form.get("name2")
        if name:
            email = request.form.get("email2")
            question = request.form.get("question")
            db.session.add(Questions(name=name, email=email, question=question, status="Pending", answer=""))
            db.session.commit()
            flash(f"{name}'s question asked!", "info")
    return render_template("submit.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)