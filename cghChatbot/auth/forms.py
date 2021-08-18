from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, Email, EqualTo, NumberRange, ValidationError
from ..models import *

class RegistrationForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=20)], render_kw={"autocomplete":"off", "placeholder":"First Name"})
    lastname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=20)], render_kw={"autocomplete":"off", "placeholder":"Last Name"})
    email = StringField("Email",validators=[DataRequired(), Email()], render_kw={"autocomplete":"off", "placeholder":"Email Address"})
    password = PasswordField("Password",validators=[DataRequired()], render_kw={"autocomplete":"off", "placeholder":"Password"})
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(), EqualTo("password")], render_kw={"autocomplete":"off", "placeholder":"Confirm Password"})
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This email is already taken.")

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()], render_kw={"autocomplete":"off", "autofocus":"True", "placeholder":"Email Address"})
    password = PasswordField("Password",validators=[DataRequired()], render_kw={"autocomplete":"off", "placeholder":"Password"})
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RequestResetForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()], render_kw={"autocomplete":"off", "autofocus":"True", "placeholder":"Email Address"})
    submit = SubmitField("Continue")

    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError("There is no account with that email. You must register first.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password",validators=[DataRequired()], render_kw={"autocomplete":"off", "placeholder":"New Password"})
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(), EqualTo("password")], render_kw={"autocomplete":"off", "placeholder":"Confirm Password"})
    submit = SubmitField("Reset Password")