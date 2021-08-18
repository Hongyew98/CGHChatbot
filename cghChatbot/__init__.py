from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from .config import Config


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
login_manager.login_view = "login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .auth.routes import auth
    app.register_blueprint(auth)

    from .admin.routes import admin
    app.register_blueprint(admin)

    from .user.routes import user
    app.register_blueprint(user)

    from .chatbot.routes import bot
    app.register_blueprint(bot)

    return app