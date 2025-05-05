from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, TextAreaField, SubmitField, FileField, MultipleFileField
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
    novel_avatar = FileField('Загрузить обложку новеллы', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения (.png, .jpg, .jpeg) разрешены')
    ])
    novel_pics = MultipleFileField('Загрузить скриншоты, трейлер новеллы', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'mkv'],
                    'Только изображения или видео форматы (jpg, jpeg, png, gif, mp4, avi, mov, mkv)')
    ])
    submit = SubmitField()
