from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField, FileField,
                     MultipleFileField, BooleanField)
from flask_wtf.file import FileAllowed
from wtforms.widgets import ListWidget, CheckboxInput


class EditNovel(FlaskForm):
    name = StringField('Новое название лучше не бывает')
    genre = SelectMultipleField('Новые жанры - прекрасное дополнение к новелле', coerce=int, option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    age_limit = SelectField('Возрастное ограничение подбираете с умом', coerce=int)
    desc = TextAreaField('Новое описание - украшение вашей новеллы')
    novel_ava = FileField('Новая славная обложка для новеллы',
                          validators=[FileAllowed(['png', 'jpg', 'jpeg'], 'Поддерживаем только форматы изображений')])
    novel_arch = FileField('Другая новелла изумительна',
                           validators=[FileAllowed(['zip', 'rar', '7z'], 'Поддерживаем только форматы .zip, .rar, .7z')])
    novel_pics = MultipleFileField('Новые великолепные скриншоты и/или трейлер новеллы',
                                   validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'mkv'],
                    'Поддерживаем только форматы изображений или видео (jpg, jpeg, png, gif, mp4, avi, mov, mkv)')])
    del_old_scr = BooleanField('Удалить старые скриншоты/трейлер новеллы')
    submit = SubmitField('Сохранить')
