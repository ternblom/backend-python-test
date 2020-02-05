from alayatodo._main import bp
from flask import render_template


@bp.route('/')
def home():
  with bp.open_resource('../../README.md', mode='r') as f:
    readme = f.read()
    return render_template('index.html', readme=readme)