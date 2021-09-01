from functools import wraps
from flask import flash, current_app, request, redirect, url_for
from flask_login import current_user, login_fresh
from ..models import *

def admin_required(func): # modified fresh_login_required method
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in set(['OPTIONS']) or \
        current_app.config.get('LOGIN_DISABLED'):
            pass
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not login_fresh():
            return current_app.login_manager.needs_refresh()
        elif not current_user.admin():
            flash("You do not have permission to access this page.", "warning")
            return redirect(url_for("user.index"))
        # from source code
        try:
            return current_app.ensure_sync(func)(*args, **kwargs)
        except AttributeError:
            return func(*args, **kwargs)
    return decorated_view
    

# edit to send cv to hr email
from flask import url_for
from flask_mail import Message
from cghChatbot import mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("CGH Password Reset Request", sender="noreply@cgh.com", recipients=[user.email])
    msg.body = f'''To reset your password, click on the following link:
{url_for('auth.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email.
    '''
    mail.send(msg)