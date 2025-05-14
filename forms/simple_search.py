from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField


class SimpleSearch(FlaskForm):
    simple_search = StringField()
    submit = SubmitField('🔍')