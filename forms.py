from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, Email, EqualTo, ValidationError
from .models import *

class RegistrationForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Validation Message")

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    cv = FileField("Upload CV", validators=[FileAllowed(["doc", "docx", "pdf"], "word or pdf only!")])
    submit = SubmitField("Upload")

    # def validate_cv(self, cv):
    #     if cv.data:
    #         cv.data = re.sub(r'[^a-z0-9_.-]', '_', cv.data)

class JobForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    type = SelectField("Type", validators=[DataRequired()], choices=["Full Time", "Part Time", "Intern"])
    minpay = IntegerField("Min Pay", validators=[DataRequired()])
    maxpay = IntegerField("Max Pay", validators=[DataRequired()])
    submit = SubmitField("Create")