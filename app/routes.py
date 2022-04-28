from flask import render_template, redirect, url_for, flash
from app import db, models, process_app
from app.forms import AddEmployee


@process_app.route('/')
def test():
    return "dasdasda"


@process_app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = AddEmployee()
    if form.validate_on_submit():
        new_user = models.Employee(first_name=form.first_name.data,
                                   last_name=form.last_name.data,
                                   password=form.password,
                                   admin=form.admin.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("test"))
    return render_template('signup.html', form=form)
