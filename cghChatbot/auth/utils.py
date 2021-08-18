from flask import url_for
from flask_mail import Message
from cghChatbot import mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[user.email])
    msg.body = f'''To reset your password, click on the following link:
{url_for('auth.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email.
    '''
    mail.send(msg)