from wtforms import (
    StringField,
    SubmitField
)
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class DepartmentForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    members = StringField('Работники', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    
    submit = SubmitField('Создать')