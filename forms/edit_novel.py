from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField, FileField,
                     MultipleFileField, BooleanField)
from flask_wtf.file import FileAllowed
from wtforms.widgets import ListWidget, CheckboxInput


class EditNovel(FlaskForm):
    name = StringField('Название')
    genre = SelectMultipleField('Жанр', coerce=int, option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    age_limit = SelectField('Ограничение', coerce=int)
    desc = TextAreaField('Описание')
    novel_ava = FileField('Загрузите обложку файлов',
                          validators=[FileAllowed(['png', 'jpg', 'jpeg'], 'Только форматы изображений')])
    novel_arch = FileField('Загрузите архив новеллы',
                           validators=[FileAllowed(['zip', 'rar', '7z'], 'Только форматы .zip, .rar, .7z')])
    novel_pics = MultipleFileField('Загрузите трейлер/скриншоты новеллы',
                                   validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'mkv'],
                    'Только изображения или видео форматы (jpg, jpeg, png, gif, mp4, avi, mov, mkv)')])
    del_old_scr = BooleanField('Удалить старые скриншоты')
    submit = SubmitField('Сохранить')
