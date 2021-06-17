"""Create a form for picking the schedule date."""

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import DateField

class ScheduleDatePicker(FlaskForm):
    """Create a form for selecting the schedule date."""

    gamedate = DateField("DatePicker", format="%Y-%m-%d", default=datetime.today)
    submit = SubmitField("Go")
