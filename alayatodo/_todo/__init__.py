from flask import Blueprint

bp = Blueprint('_todo', __name__)

from alayatodo._todo import routes