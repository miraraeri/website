from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField
from wtforms.widgets import ListWidget, CheckboxInput

class EditNovel(FlaskForm):
    name = StringField('Название')
    genre = SelectMultipleField('Жанр', coerce=int, option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    age_limit = SelectField('Ограничение', coerce=int)
    desc = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
