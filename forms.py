from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, Email, EqualTo, NumberRange, ValidationError
from .models import *

class RegistrationForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=20)], render_kw={"autocomplete":"off"})
    lastname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=20)], render_kw={"autocomplete":"off"})
    email = StringField("Email",validators=[DataRequired(), Email()], render_kw={"autocomplete":"off"})
    password = PasswordField("Password",validators=[DataRequired()], render_kw={"autocomplete":"off"})
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(), EqualTo("password")], render_kw={"autocomplete":"off"})
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Validation Message")

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()], render_kw={"autocomplete":"off", "autofocus":"True"})
    password = PasswordField("Password",validators=[DataRequired()], render_kw={"autocomplete":"off"})
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    cv = FileField("Upload CV", validators=[FileAllowed(["doc", "docx", "pdf"], "word or pdf only!")])
    submit = SubmitField("Upload")

    # def validate_cv(self, cv):
    #     if cv.data:
    #         cv.data = re.sub(r'[^a-z0-9_.-]', '_', cv.data)

class JobForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()], render_kw={"autocomplete":"off"})
    description = TextAreaField("Description", validators=[DataRequired()])
    type = SelectField("Type", validators=[DataRequired()], choices=["Full Time", "Part Time", "Intern"])
    minpay = IntegerField("Min Pay", validators=[DataRequired()], render_kw={"autocomplete":"off"})
    maxpay = IntegerField("Max Pay", validators=[DataRequired()], render_kw={"autocomplete":"off"})
    submit = SubmitField("Save")

#class QuestionForm(FlaskForm):
