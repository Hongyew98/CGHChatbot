from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from ..models import *

class CreateForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired(), Length(min=2, max=30)], render_kw={"autocomplete":"off", "placeholder":"Job Title"})
    duration = IntegerField("Duration(in min)", validators=[DataRequired()], render_kw={"autocomplete":"off", "placeholder":"Duration(in min)"})
    questions = IntegerField("Questions to display", validators=[DataRequired()], render_kw={"autocomplete":"off", "placeholder":"Questions to display"})
    submit = SubmitField("Create")

    def validate_jobtitle(self, title):
        if Job.query.filter_by(title=title.data).first():
            raise ValidationError("This email is already taken.")

class EditForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired(), Length(min=2, max=30)], render_kw={"autocomplete":"off", "placeholder":"Job Title"})
    duration = IntegerField("Duration(in min)", validators=[DataRequired()], render_kw={"autocomplete":"off", "placeholder":"Duration(in min)"})
    questions = IntegerField("Questions to display", validators=[DataRequired()], render_kw={"autocomplete":"off", "placeholder":"Questions to display"})
    submit = SubmitField("Submit")