from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, models, process_app
from app.forms import AddEmployee


@process_app.route('/')
def test():
    return render_template('base.html')


@process_app.route('/login')
def login():
    return render_template('login.html')


@process_app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = bool(request.form.get('remember'))

    user = models.Employee.query.filter_by(user_name=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('test'))


@process_app.route('/signup')
def signup():
    form = AddEmployee()
    return render_template('signup.html', form=form)


@process_app.route('/signup', methods=['POST'])
def signup_post():
    form = AddEmployee()
    if form.validate_on_submit():
        new_user = models.Employee(first_name=form.first_name.data,
                                   last_name=form.last_name.data,
                                   user_name=form.user_name.data,
                                   password=generate_password_hash(form.password.data, method='sha256'),
                                   admin=form.admin.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("test"))
    return render_template('signup.html', form=form)


@process_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('test'))
