"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
import subprocess
import os

from flask_migrate import upgrade
from alayatodo import app
from alayatodo.helpers import db_seed


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        with app.app_context():
            upgrade()
            print("AlayaTodo: Database initialized.")
            db_seed()
            print("AlayaTodo: Database seed data ready.")
    else:
        app.run(use_reloader=True)
