from app import db
from flask_login import UserMixin

product_processes = db.Table('product_processes',
                             db.Column('Product', db.Integer, db.ForeignKey('product.product_id')),
                             db.Column('Process', db.Integer, db.ForeignKey('process.process_id'))
                             )

orders_products = db.Table('orders_products',
                           db.Column('Order', db.Integer, db.ForeignKey('order.order_id')),
                           db.Column('Product', db.Integer, db.ForeignKey('product.product_id'))
                           )


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column("Name", db.String)
    processes = db.relationship("Process", secondary=product_processes, back_populates="products")
    orders = db.relationship("Order", secondary=orders_products, back_populates="products")


class Process(db.Model):
    process_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column("Name", db.String)
    responsible_employee = db.Column(db.Integer, db.ForeignKey('employee.id'))
    products = db.relationship("Product", secondary=product_processes, back_populates="processes")
    processes_in_order = db.relationship('ProcessInOrder', backref='Process', lazy='dynamic')


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, nullable=False)
    customer = db.Column("Name", db.String)
    quantity = db.Column("Quantity", db.Integer)
    completed = db.Column("Completed", db.Boolean, default=False)
    date_to_complete = db.Column("Date_to_complete", db.Date)
    products = db.relationship("Product", secondary=orders_products, back_populates="orders")
    processes_in_order = db.relationship('ProcessInOrder', backref='Order', lazy='dynamic')


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column("First name", db.String)
    last_name = db.Column("Last name", db.String)
    user_name = db.Column("Username", db.String, unique=True)
    password = db.Column("Password", db.String)
    admin = db.Column("Administrator", db.Boolean, default=False)
    processes = db.relationship('Process', backref='employee', lazy='dynamic')


class ProcessInOrder(db.Model):
    processes_in_order_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    order = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    process = db.Column(db.Integer, db.ForeignKey('process.process_id'))
    completed = db.Column("Completed", db.Boolean, default=False)
    comment = db.Column("Comment", db.String, default="")
