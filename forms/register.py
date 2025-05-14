from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Придумайте неповторимый псевдоним', validators=[DataRequired()])
    birth_date = DateField()
    email = EmailField('Введите лучшую почту', validators=[DataRequired()])
    password = PasswordField('Придумайте оригинальный пароль', validators=[DataRequired()])
    password_again = PasswordField('Не забудьте его повторить', validators=[DataRequired()])
    avatar = FileField('Загрузите любимую аватарку', validators=[
        FileRequired(),
        FileAllowed(['png', 'jpg', 'jpeg'], 'Поддерживаем только форматы .png, .jpg, .jpeg')
    ])
    submit = SubmitField('Час регистрации настал')
