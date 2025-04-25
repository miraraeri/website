from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Псевдоним', validators=[DataRequired()])
    birth_date = DateField()
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    avatar = FileField('Загрузите фото', validators=[
        # FileRequired(),
        FileAllowed(['png', 'jpg', 'jpeg'], 'Только форматы .png, .jpg, .jpeg')
    ])
    submit = SubmitField('Зарегистрироваться')
