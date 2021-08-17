from os import name
from flask import current_app
from datetime import datetime
from flask_login import UserMixin

if __name__ == "__main__":
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    from config import Config

    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    login_manager = LoginManager(app)

    # Uncomment following to edit db schema
    # from flask_migrate import Migrate
    # migrate = Migrate(app, db)
    
    db.create_all()

else:
    from cghChatbot import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cv = db.Column(db.String(30), default="")
    application = db.relationship("Application", backref="applicant", lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}','{self.email}')"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer)
    status = db.Column(db.String, default="Applied")
    comments = db.Column(db.Text, default="")
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Details('{self.job}','{self.cv}','{self.score}','{self.status}')"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    question = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, default="Pending")
    answer = db.Column(db.Text, default="")
    date_asked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Details('{self.job}','{self.cv}','{self.score}','{self.status}')"