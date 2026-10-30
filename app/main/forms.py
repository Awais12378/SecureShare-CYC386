from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from app.config import Config


class FileUploadForm(FlaskForm):
    """File upload form with validation."""
    
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(Config.ALLOWED_EXTENSIONS, 'Invalid file type. Allowed types: txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx')
    ])
    description = TextAreaField('Description (optional)', validators=[Length(max=500)])
    submit = SubmitField('Upload')


class FileShareForm(FlaskForm):
    """File sharing form."""
    
    username = StringField('Share with user', validators=[DataRequired()])
    permission = SelectField('Permission', choices=[('read', 'Read Only'), ('write', 'Read/Write')], default='read')
    submit = SubmitField('Share File')
