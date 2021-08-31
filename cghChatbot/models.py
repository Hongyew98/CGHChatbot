from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

if __name__ == "__main__":
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    from config import Config

    current_app = Flask(__name__)
    current_app.config.from_object(Config)
    db = SQLAlchemy(current_app)
    login_manager = LoginManager(current_app)


else:
    from flask import current_app
    from cghChatbot import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.png")
    password = db.Column(db.String(60), nullable=False)
    cv = db.Column(db.String(30), default="")
    cvname = db.Column(db.String(30), default="")
    application = db.relationship("Application", backref="applicant", lazy=True)
    role = db.Column(db.Boolean, default=0)

    def get_reset_token(self, expires_sec=180):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    def admin(self):
        return self.role

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}','{self.email}')"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer)
    status = db.Column(db.String, default="Applied")
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Application('{self.job}','{self.score}','{self.status}')"


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    question = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, default="Pending")
    answer = db.Column(db.Text, default="")
    date_asked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Details('{self.email}','{self.question}','{self.answer}','{self.status}')"

if __name__ == "__main__":
    db.create_all()