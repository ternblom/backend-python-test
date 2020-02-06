import json
from flask import request, current_app as app
from alayatodo import db
from alayatodo.models import User, Todo


def db_seed():
  with open('resources/default_data.json') as jf:
    data = json.load(jf)
    for u in data.get('users'):
      user = User(username=u['username'])
      user.set_password(u['password'])
      db.session.add(user)
      for t in u['todos']:
        db.session.add(Todo(description=t['description'], completed=False, user=user))
    db.session.commit()

def get_pagination_info():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', app.config['TODOS_PER_PAGE'], type=int)
  todo_filter_by = request.args.get('todo_filter_by', app.config['TODOS_DEFAULT_FILTER'])

  if not request.args.get('per_page') and not request.args.get('per_page'):
      if request.cookies.get('TODOS_ACTIVE_PAGE'):
          page = int(request.cookies.get('TODOS_ACTIVE_PAGE'))
          per_page = int(request.cookies.get('TODOS_PER_PAGE'))

  if not request.args.get('todo_filter_by'):
      if request.cookies.get('TODOS_FILTER_BY'):
          todo_filter_by = request.cookies.get('TODOS_FILTER_BY')

  return page, per_page, todo_filter_by
