from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# This form collects data to register a cargo package
class PackageForm(FlaskForm):
    sender_name = StringField(
        "Sender Name",
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    receiver_name = StringField(
        "Receiver Name",
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    phone_sender = StringField(
        "Sender Phone",
        validators=[DataRequired(), Length(min=10, max=15)]
    )
    phone_receiver = StringField(
        "Receiver Phone",
        validators=[DataRequired(), Length(min=10, max=15)]
    )
    submit = SubmitField("Register Package")