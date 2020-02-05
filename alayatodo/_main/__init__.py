from flask import Blueprint

bp = Blueprint('_main', __name__)

from alayatodo._main import routes
