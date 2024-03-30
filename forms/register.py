from wtforms import (
    StringField, 
    IntegerField,
    PasswordField, 
    SubmitField
)
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    login = StringField('Login / email', validators=[DataRequired()])
    pwd1 = PasswordField('Password', validators=[DataRequired()])
    pwd2 = PasswordField('Repeat password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    adress = StringField('Addrees', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')