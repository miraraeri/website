from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import StringField, DateField, EmailField, PasswordField, FileField, SubmitField


class EditUserForm(FlaskForm):
    username = StringField('Псевдоним')
    birth_date = DateField()
    email = EmailField('Почта')
    password = PasswordField('Пароль')
    avatar = FileField('Загрузите файл',
                       validators=[FileAllowed(['png', 'jpg', 'jpeg'],
                                               'Только форматы .png, .jpg, .jpeg')])
    submit = SubmitField('Сохранить')
