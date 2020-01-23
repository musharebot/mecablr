from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class TextForm(FlaskForm):
    name = StringField('Paste japanese below', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Submit')