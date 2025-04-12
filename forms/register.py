from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Псевдоним', validators=[DataRequired()])
    birth_date = DateField()
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    avatar = FileField('Загрузите фото')
    submit = SubmitField('Зарегистрироваться')
