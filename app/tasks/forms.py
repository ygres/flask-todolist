from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeLocalField, BooleanField
from wtforms.validators import DataRequired


class TasksCreateForm(FlaskForm):
    name = StringField('Название', [DataRequired(message="Поле обязательно для заполнения")])
    deadline = DateTimeLocalField("Срок выполнения", format="%Y-%m-%dT%H:%M")

class TasksUpdateForm(FlaskForm):
    name = StringField('Название', [DataRequired(message="Поле обязательно для заполнения")])
    deadline = DateTimeLocalField("Срок выполнения", format="%Y-%m-%dT%H:%M")
    completed = BooleanField("Завершена")
