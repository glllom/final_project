from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_login import LoginManager

process_app = Flask(__name__, template_folder="templates")
process_app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(process_app)
migrate = Migrate(process_app, db)

login_manager = LoginManager()
login_manager.login_view = 'routes.login'
login_manager.init_app(process_app)

from app.models import Employee


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


from app import models, routes

db.create_all(app=process_app)
