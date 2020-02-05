import os
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


# configuration
DATABASE = '/tmp/alayatodo.db'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + DATABASE
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = '_auth.login'
login_manager.login_message_category = 'info'

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
