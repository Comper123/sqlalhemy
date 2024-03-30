from wtforms import (
    BooleanField,
    StringField,
    IntegerField,
    SubmitField
)
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class JobForm(FlaskForm):
    job = StringField('Работа', validators=[DataRequired()])
    work_size = IntegerField('Время работы', validators=[DataRequired()])
    collaborators = StringField('Работники', validators=[DataRequired()])
    is_finished = BooleanField('Завершена?')
    
    submit = SubmitField('Создать')