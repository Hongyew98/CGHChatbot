from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo, Email, EqualTo, Length, Regexp, ValidationError
from flask_wtf.file import FileAllowed
from ..models import *
from .utils import *

class CVForm(FlaskForm):
    cv = FileField("Upload CV", validators=[FileAllowed(["doc", "docx", "pdf"])])
    submit = SubmitField("Next")

class UpdateAccountForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()], render_kw={"autocomplete":"off", "placeholder":"Email Address"})
    image = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    cv = FileField("Upload CV", validators=[FileAllowed(["doc", "docx", "pdf"])])
    password = PasswordField("Current Password", render_kw={"autocomplete":"off", "placeholder":"Current Password"})
    new_password = PasswordField("Password", validators=[Length(min=8, message="Password should contain min 8 characters."),
                                                     Regexp("^(?=.*[A-Za-z])(?=.*\d)([A-Za-z\d]+)$", message="Password should contain at least 1 letter and 1 number."),
                                                     DataRequired()], render_kw={"autocomplete":"off", "placeholder":"Password"})
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords do not match.")], render_kw={"autocomplete":"off", "placeholder":"Confirm Password"})
    submit = SubmitField("Save")

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("This email is already taken.")

    def validate_password(self, password):
        if password.data:
            if generate_password_hash(password.data, method='sha256') != current_user.password:
                raise ValidationError("Incorrect password.")