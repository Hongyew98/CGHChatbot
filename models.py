from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask_migrate import Migrate

#To edit db schema
#migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    applications = db.relationship("Application", backref="applicant", lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}','{self.email}')"

class Applications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100), nullable=False)
    cv = db.Column(db.String(30))
    score = db.Column(db.Integer)
    status = db.Column(db.String)
    comments = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"Details('{self.job}','{self.cv}','{self.score}','{self.status}')"

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    question = db.Column(db.Text, nullable=False)
    status = db.Column(db.String)
    answer = db.Column(db.String)
    date_asked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

if __name__ == "__main__":
    db.create_all()