from flask import Blueprint

bp = Blueprint('_auth', __name__)

from alayatodo._auth import routes