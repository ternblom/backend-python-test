from flask import Blueprint

bp = Blueprint('_errors', __name__)

from alayatodo._errors import handlers