from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectMultipleField
from wtforms.validators import InputRequired, EqualTo


class AddEmployee(FlaskForm):
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    user_name = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    admin = BooleanField("Administrator")
    submit = SubmitField()


class AddProduct(FlaskForm):
    Name = StringField("Name of Product", validators=[InputRequired()])
    Processes = SelectMultipleField("Processes")
    submit = SubmitField()


class AddProcess(FlaskForm):
    Name = StringField("Name of process", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    user_name = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    admin = BooleanField("Administrator")
    submit = SubmitField()


