from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import StringField, DateField, EmailField, PasswordField, FileField, SubmitField


class EditUserForm(FlaskForm):
    username = StringField('Новый псевдоним такой же неповторимый')
    birth_date = DateField()
    email = EmailField('Новая почта - новая жизнь')
    password = PasswordField('Новый пароль - это прекрасно. Оставьте поле пустым, если не хотите изменений')
    avatar = FileField('Новая аватарка будет так же любима',
                       validators=[FileAllowed(['png', 'jpg', 'jpeg'],
                                               'Всё также поддерживаем только форматы .png, .jpg, .jpeg')])
    submit = SubmitField('Сохранение изменений')
