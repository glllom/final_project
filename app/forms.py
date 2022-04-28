from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import InputRequired, EqualTo


class AddEmployee(FlaskForm):
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    password_confirm = StringField("Confirm Password", validators=[InputRequired(), EqualTo(password)])
    admin = BooleanField("Administrator")
    submit = SubmitField()
