from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from datetime import date


class CreateNovel(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    creation_date = DateField(default=date.today())
    genre = StringField('Жанр')
    age_limit = StringField('Ограничение')
    desc = TextAreaField('Описание')
    novel_arch = FileField('Загрузить новеллу', validators=[
        FileRequired(),
        FileAllowed(['zip', 'rar', '7z'], 'Только архивы (.zip, .rar, .7z) разрешены')
    ])
    submit = SubmitField()
