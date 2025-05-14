from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Ваша почта', validators=[DataRequired()])
    password = PasswordField('Ваш пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомним и не будем беспокоить 30 дней')
    submit = SubmitField('Входите в незабываемый мир историй')
