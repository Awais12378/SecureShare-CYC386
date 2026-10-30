from flask_wtf import FlaskForm
from wtforms import SubmitField


class EmptyForm(FlaskForm):
    """Empty form for CSRF protection on POST requests without form fields."""
    submit = SubmitField('Submit')
