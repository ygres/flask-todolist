from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginCreateForm(FlaskForm):
    username = StringField('Логин', [DataRequired(message="Поле обязательно для заполнения")])
    password = PasswordField('Пароль', [DataRequired(message="Поле обязательно для заполнения")])

class RegisterCreateForm(FlaskForm):
    username = StringField('Логин', [DataRequired(message="Поле обязательно для заполнения")])
    email = StringField('Email', [Email()])
    password = PasswordField('Пароль', [DataRequired(message="Поле обязательно для заполнения")])
