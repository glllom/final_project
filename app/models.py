from app import db

# product_processes = db.Table('product_processes',
#                              db.Column('product', db.Integer, db.ForeignKey('product.product_id')),
#                              db.Column('process', db.Integer, db.ForeignKey('process.process_id'))
#                              )
#
# orders_products = db.Table('orders_products',
#                            db.Column('order', db.Integer, db.ForeignKey('order.order_id')),
#                            db.Column('product', db.Integer, db.ForeignKey('product.product_id'))
#                            )
#
#
# class Product(db.Model):
#     product_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
#     name = db.Column("Name", db.String)
#     processes = db.relationship("process", secondary=product_processes, back_populates="products")
#     orders = db.relationship("order", secondary=orders_products, back_populates="products")
#
#
# class Process(db.Model):
#     process_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
#     name = db.Column("Name", db.String)
#     comment = db.Column("Comment", db.String)
#     completed = db.Column("Completed", db.Boolean, default=False)
#     responsible_employee = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
#     products = db.relationship("product", secondary=product_processes, back_populates="processes")
#
#
# class Order(db.Model):
#     order_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     customer = db.Column("Name", db.String)
#     completed = db.Column("Completed", db.Boolean, default=False)
#     products = db.relationship("product", secondary=orders_products, back_populates="orders")
#     date_to_complete = db.Column("Date_to_complete", db.Date)


class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column("First name", db.String)
    last_name = db.Column("Last name", db.String)
    password = db.Column("Password", db.String)
    admin = db.Column("Administrator", db.Boolean, default=False)
    # processes = db.relationship('process', backref='employee', lazy='dynamic')
