from flask import Flask, g
import sqlite3

# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)

# blueprints
from alayatodo._auth import bp as _auth_bp
app.register_blueprint(_auth_bp)

from alayatodo._todo import bp as _todo_bp
app.register_blueprint(_todo_bp)

from alayatodo._main import bp as _main_bp
app.register_blueprint(_main_bp)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
