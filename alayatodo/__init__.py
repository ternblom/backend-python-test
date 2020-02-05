import os
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from alayatodo.config import Config


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
bcrypt = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = '_auth.login'
login_manager.login_message_category = 'info'

def create_app(config_object=Config):
  app = Flask(__name__)
  app.config.from_object(config_object)

  db.init_app(app)
  migrate.init_app(app, db)
  ma.init_app(app)
  bcrypt.init_app(app)
  csrf.init_app(app)
  login_manager.init_app(app)

  # blueprints
  from alayatodo._auth import bp as _auth_bp
  app.register_blueprint(_auth_bp)

  from alayatodo._todo import bp as _todo_bp
  app.register_blueprint(_todo_bp)

  from alayatodo._errors import bp as _errors_bp
  app.register_blueprint(_errors_bp)

  from alayatodo._main import bp as _main_bp
  app.register_blueprint(_main_bp)

  from alayatodo import models

  return app
