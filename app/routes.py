from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, models, process_app
from app.forms import AddEmployee, AddProduct, AddProcess, AddOrder


@process_app.route('/dashboard')
def dashboard():
    return render_template('homepage.html')


@process_app.route('/')
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
    login_user(user, remember=remember)
    return redirect(url_for('dashboard'))


@process_app.route('/signup')
def signup():
    form = AddEmployee()
    return render_template('signup.html', form=form)


@process_app.route('/signup', methods=['POST'])
@login_required
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
        return redirect(url_for("homepage"))
    return render_template('signup.html', form=form)


@process_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@process_app.route('/add_product', methods=['get', 'post'])
@login_required
def add_product():
    form = AddProduct()
    form.processes.choices = [
        (process.process_id, process.name) for process in models.Process.query.all()
    ]
    if form.is_submitted():
        new_product = models.Product(name=form.name.data)
        db.session.add(new_product)
        db.session.commit()
    return render_template('add_product.html', form=form)


@process_app.route('/add_process', methods=['get', 'post'])
@login_required
def add_process():
    form = AddProcess()
    form.employee.choices = [
        (employee.id, f"{employee.first_name} {employee.last_name}") for employee in models.Employee.query.all()
    ]
    form.products.choices = [
        (product.product_id, product.name) for product in models.Product.query.all()
    ]
    if form.is_submitted():
        new_process = models.Process(name=form.name.data,
                                     employee=models.Employee.query.get(form.employee.data),
                                     products=[
                                         models.Product.query.get(product)
                                         for product in form.products.data
                                     ])
        db.session.add(new_process)
        db.session.commit()
    return render_template('add_process.html', form=form)


@process_app.route('/add_order', methods=['get', 'post'])
@login_required
def add_order():
    form = AddOrder()
    form.product.choices = [
        (product.product_id, product.name) for product in models.Product.query.all()
    ]
    if form.is_submitted():
        order_id = form.order_id.data
        products = [models.Product.query.get(product)
                    for product in form.product.data]
        for process in products[0].processes:
            new_process_in_order = models.ProcessInOrder(specified_order=order_id,
                                                         process=process)
            db.session.add(new_process_in_order)
        new_order = models.Order(order_id=order_id,
                                 date_to_complete=form.date.data,
                                 products=products)
        db.session.add(new_order)
        db.session.commit()
    return render_template('add_order.html', form=form)
