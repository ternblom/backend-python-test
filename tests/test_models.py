import unittest
from alayatodo import db
from alayatodo.models import User, Todo, TodoSchema
from alayatodo.helpers import db_seed
from . import app

class TestUserModel(unittest.TestCase):
  
  def setUp(self):
    db.app = app
    db.create_all()
    db_seed()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_user_save(self):
    """
    Should exist the user1 in the database
    """
    user = User.query.filter_by(username='user1').one()
    assert user is not None
    assert user.__repr__() == "User('user1')"

  def test_user_password(self):
    """
    Should the password of the user1 be "user1"
    """
    user = User.query.filter_by(username='user1').one()
    assert user.check_password('user1')


class TestToDoModel(TestUserModel):

  def test_todo_description(self):
    """
    Should raise an exception if ToDo has the description 
      - empty 
      - fill in with white space
    """
    user = User.query.filter_by(username='user1').one()

    with self.assertRaises(AssertionError):
      Todo(description='', user=user)  

    with self.assertRaises(AssertionError):
      Todo(description='  ', user=user)  

  def test_add_todo(self):
    """
    Should the ToDo exist in the database
    """
    user = User.query.filter_by(username='user1').one()
    todo = Todo(description='My First Todo', user=user)
    db.session.add(todo)
    db.session.commit()

    _todo = Todo.query.get(todo.id)

    assert _todo == todo

  def test_todo_users(self):
    """
    ./resources/default_data.json
    user1 with id 1 has to have 6 ToDo
    user2 with id 2 has to have 5 ToDo
    """  
    user1_todos = Todo.query.filter_by(user=User.query.get(1)).all()
    user2_todos = Todo.query.filter_by(user=User.query.get(2)).all()

    assert len(user1_todos) == 6
    assert len(user2_todos) == 5

  def test_todo_repr(self):
    """
    ./resources/default_data.json
    user1 first ToDo should be
     - Todo('Ad laborum ea culpa cupidatat commodo do.')
    """  

    todo = Todo.query.filter_by(user=User.query.get(1)).first()
    assert todo.__repr__() == "Todo('Ad laborum ea culpa cupidatat commodo do.')"

  def test_todo_json(self):
    """
    ./resources/default_data.json
    user1 first ToDo formatted as a json should have this key, values
     - {
        'id': 1, 
        'user_id': 1, 
        completed': False, 
        'description': 
        'Ad laborum ea culpa cupidatat commodo do.'
      }
    """  
    todo_schema = TodoSchema()
    todo = Todo.query.filter_by(user=User.query.get(1)).first()
    json = todo_schema.dump(todo)

    assert json.get('id') == 1
    assert json.get('user_id') == 1
    assert json.get('completed') == False
    assert json.get('description') == 'Ad laborum ea culpa cupidatat commodo do.'
