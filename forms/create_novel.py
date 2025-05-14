from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, TextAreaField, SubmitField, FileField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from datetime import date


class CreateNovel(FlaskForm):
    name = StringField('Придуймайте достойное название', validators=[DataRequired()])
    creation_date = DateField(default=date.today())
    genre = StringField('Выберите подходящие жанры')
    age_limit = StringField('Не забудьте про возрастное ограничение')
    desc = TextAreaField('Напишите бесподобное описание')
    novel_arch = FileField('Загрузите превосходную новеллу', validators=[
        FileRequired(),
        FileAllowed(['zip', 'rar', '7z'], 'Поддерживаем только архивы (.zip, .rar, .7z) разрешены')
    ])
    novel_avatar = FileField('Загрузите идеальную обложку для новеллы', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Поддерживаем только изображения (.png, .jpg, .jpeg) разрешены')
    ])
    novel_pics = MultipleFileField('Загрузите лучшие скриншоты и/или трейлер новеллы', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'mkv'],
                    'Поддерживаем только форматы изображений или видео (jpg, jpeg, png, gif, mp4, avi, mov, mkv)')
    ])
    submit = SubmitField()
