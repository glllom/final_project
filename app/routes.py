from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, models, process_app
from app.forms import AddEmployee, AddProduct, AddProcess, AddOrder


@process_app.route('/dashboard')
@login_required
def dashboard():
    table = [process for process in models.ProcessInOrder.query.filter_by(completed=False) if
             process.Process.responsible_employee == current_user.id]
    return render_template('homepage.html', table=table)


@process_app.route('/complete_process/<int:process_id>', methods=['get', 'post'])
@login_required
def complete_process(process_id):
    order = models.ProcessInOrder.query.get(process_id).Order
    print(order)
    models.ProcessInOrder.query.get(process_id).completed = True
    if not list(models.ProcessInOrder.query.filter_by(completed=False, order=order.order_id)):
        order.completed = True
    db.session.commit()
    return redirect(url_for('dashboard'))


# Login / Logout
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


@process_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Add user/ Remove user
@process_app.route('/add_user')
@login_required
def add_user():
    if not current_user.admin:
        return redirect(url_for('login'))
    form = AddEmployee()
    table = models.Employee.query.filter(models.Employee.id > 1, models.Employee.active)
    return render_template('add_user.html', form=form, table=table)


@process_app.route('/add_user', methods=['POST'])
@login_required
def add_user_post():
    form = AddEmployee()
    if form.validate_on_submit():
        if form.user_name.data in [user.user_name for user in models.Employee.query.all()]:
            flash("This username already used.")
            return redirect(url_for("add_user"))
        new_user = models.Employee(first_name=form.first_name.data,
                                   last_name=form.last_name.data,
                                   user_name=form.user_name.data,
                                   password=generate_password_hash(form.password.data, method='sha256'),
                                   admin=form.admin.data)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for("add_user"))


@process_app.route('/remove_user/<int:user_id>')
@login_required
def remove_user(user_id):
    models.Employee.query.get(user_id).active = False
    db.session.commit()
    return redirect(url_for("add_user"))


# Product operations
@process_app.route('/add_product', methods=['get', 'post'])
@login_required
def add_product():
    if not current_user.admin:
        return redirect(url_for('dashboard'))
    table = models.Product.query.filter(models.Product.active)
    form = AddProduct()
    form.processes.choices = [
        (process.process_id, process.name) for process in models.Process.query.filter(models.Process.active)
    ]
    if form.is_submitted():
        new_product = models.Product(name=form.name.data,
                                     processes=[
                                         models.Process.query.get(product)
                                         for product in form.processes.data
                                     ])
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('add_product'))
    return render_template('add_product.html', form=form, table=table)


@process_app.route('/change_product/<int:product_id>', methods=['post'])
@login_required
def change_product(product_id):
    if not current_user.admin:
        return redirect(url_for('dashboard'))
    table = models.Product.query.filter(models.Product.active)
    form = AddProduct()
    form.processes.choices = [
        (process.process_id, process.name) for process in models.Process.query.filter(models.Process.active)
    ]
    if form.is_submitted():
        product_to_change = models.Product.query.get(product_id)
        product_to_change.name = form.name.data
        product_to_change.processes = [models.Process.query.get(product) for product in form.processes.data]
        db.session.commit()
        return redirect(url_for('add_product'))
    return render_template('add_product.html', form=form, table=table)


@process_app.route('/remove_product/<int:product_id>')
@login_required
def remove_product(product_id):
    models.Product.query.get(product_id).active = False
    db.session.commit()
    return redirect(url_for("add_product"))


# Processes operations
@process_app.route('/add_process', methods=['get', 'post'])
@login_required
def add_process():
    if not current_user.admin:
        return redirect(url_for('dashboard'))
    table = models.Process.query.filter(models.Process.active)
    form = AddProcess()
    form.employee.choices = [
        (employee.id, f"{employee.first_name} {employee.last_name}") for employee in
        models.Employee.query.filter(models.Employee.id > 1, models.Employee.active)
    ]
    form.products.choices = [
        (product.product_id, product.name) for product in models.Product.query.filter(models.Product.active)
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
        return redirect(url_for('add_process'))
    return render_template('add_process.html', form=form, table=table)


@process_app.route('/change_process/<int:process_id>', methods=['post'])
@login_required
def change_process(process_id):
    if not current_user.admin:
        return redirect(url_for('dashboard'))
    table = models.Process.query.filter(models.Process.active)
    form = AddProcess()
    form.employee.choices = [
        (employee.id, f"{employee.first_name} {employee.last_name}") for employee in
        models.Employee.query.filter(models.Employee.id > 1, models.Employee.active)
    ]
    form.products.choices = [
        (product.product_id, product.name) for product in models.Product.query.filter(models.Product.active)
    ]
    if form.is_submitted():
        process_to_change = models.Process.query.get(process_id)
        process_to_change.name = form.name.data
        process_to_change.employee = models.Employee.query.get(form.employee.data)
        process_to_change.products = [models.Product.query.get(product)
                                      for product in form.products.data]
        db.session.commit()
        return redirect(url_for('add_process'))
    return render_template('add_process.html', form=form, table=table)


@process_app.route('/remove_process/<int:process_id>')
@login_required
def remove_process(process_id):
    models.Process.query.get(process_id).active = False
    db.session.commit()
    return redirect(url_for("add_process"))


# Orders operations
@process_app.route('/add_order', methods=['get', 'post'])
@login_required
def add_order():
    table = models.Order.query.filter_by(completed=False).order_by(models.Order.date_to_complete.asc())
    form = AddOrder()
    form.product.choices = [
        (product.product_id, product.name) for product in models.Product.query.filter(models.Product.active)
    ]
    if form.is_submitted():
        order_id = form.order_id.data
        products = [models.Product.query.get(product)
                    for product in form.product.data]
        if order_id in [order.order_id for order in models.Order.query.all()]:
            flash("This order already presents in database.")
            return redirect(url_for('add_order'))
        new_order = models.Order(order_id=order_id,
                                 date_to_complete=form.date.data,
                                 customer=form.customer.data,
                                 quantity=form.quantity.data,
                                 products=products)
        for process in products[0].processes:
            new_process_in_order = models.ProcessInOrder(Order=new_order,
                                                         Process=process)
            db.session.add(new_process_in_order)
        db.session.add(new_order)
        db.session.commit()
    return render_template('add_order.html', form=form, table=table)


@process_app.route('/remove_order/<int:order_id>')
@login_required
def remove_order(order_id):
    for process in models.ProcessInOrder.query.filter_by(order=order_id):
        db.session.delete(process)
    db.session.delete(models.Order.query.get(order_id))
    db.session.commit()
    return redirect(url_for("add_order"))


@process_app.route('/search_order', methods=['post'])
@login_required
def search_order():
    """
    :return:
    """
    order = models.Order.query.get(request.form.get("search_field"))
    if not order:
        flash("Incorrect number.")
        return redirect(url_for("add_order"))
    processes_in_order = models.ProcessInOrder.query.filter_by(order=order.order_id)
    employees = {
        processes.processes_in_order_id: f"{models.Employee.query.get(processes.Process.responsible_employee).first_name} {models.Employee.query.get(processes.Process.responsible_employee).last_name}"
        for processes in processes_in_order}
    return render_template('show_order.html', order=order, processes_in_order=processes_in_order, employees=employees)
