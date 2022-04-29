from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectMultipleField, SelectField, IntegerField, DateField
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
    name = StringField("Name of Product", validators=[InputRequired()])
    processes = SelectMultipleField("Processes")
    submit = SubmitField()


class AddProcess(FlaskForm):
    name = StringField("Name of process", validators=[InputRequired()])
    employee = SelectField("Employee in charge of this process")
    products = SelectMultipleField("Products")
    submit = SubmitField()


class AddOrder(FlaskForm):
    order_id = IntegerField("Order Number", validators=[InputRequired()])
    customer = StringField("Customer", validators=[InputRequired()])
    date = DateField("Deadline", validators=[InputRequired()])
    product = SelectField("Type of product", validators=[InputRequired()])
    submit = SubmitField()