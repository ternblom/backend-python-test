import json
from alayatodo import db
from alayatodo.models import User, Todo


def db_seed():
  with open('resources/default_data.json') as jf:
    data = json.load(jf)
    for u in data.get('users'):
      user = User(username=u['username'],password=u['password'])
      db.session.add(user)
      for t in u['todos']:
        db.session.add(Todo(description=t['description'], completed=False, user=user))
    db.session.commit()