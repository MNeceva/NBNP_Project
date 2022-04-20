from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired, Regexp, ValidationError
from flask_wtf.file import FileRequired
from ..models import Users

class UploadFilesForm(FlaskForm):
    audio_file = FileField("Прикачи аудио запис", validators=[FileRequired()])
    txt_file = FileField("Транскрипт", validators=[FileRequired()])
    upload = SubmitField("ПРИКАЧИ ЗАПИС")