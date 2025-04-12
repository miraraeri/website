from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, EmailField, PasswordField, FileField, SubmitField


class EditUserForm(FlaskForm):
    username = StringField('Псевдоним')
    birth_date = DateField()
    email = EmailField('Почта')
    password = PasswordField('Пароль')
    avatar = FileField('Загрузите файл')
    submit = SubmitField('Сохранить')
