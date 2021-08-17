from flask import url_for
from flask_mail import Message
from cghChatbot import mail

# def save_cv(form_cv):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_cv.filename) #_ is to throw away variable name
#     cv_fn = random_hex + f_ext
#     cv_path = os.path.join(auth.root_path, "static/CVs", cv_fn)
#     form_cv.save(cv_path)
#     return cv_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[user.email])
    msg.body = f'''To reset your password, click on the following link:
{url_for('auth.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email.
    '''
    mail.send(msg)