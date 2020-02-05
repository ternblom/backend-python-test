import unittest
from alayatodo import db
from alayatodo.models import User, Todo, TodoSchema
from alayatodo.helpers import db_seed
from . import app, app_protected


class TestMainRoute(unittest.TestCase):
  def setUp(self):
    db.app = app
    db.create_all()
    db_seed()
    self.client = app.test_client()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_home(self):
    """
    Should get status code 200
    """
    result = self.client.get('/')
    assert result.status_code == 200


class TestAuthRoute(TestMainRoute):

  def test_login(self):
    """
    Should get status code 200
    """
    result = self.client.get('/login')
    assert result.status_code == 200

  def test_user_logged_in(self):
    """
    Should redirect if the user is logged in
    status code should be 302
    """
    result = self.client.post('/login', data=dict(
      username='user1',
      password='user1'
    ), follow_redirects=True)
    assert b'user1 Logout' in result.data
    assert result.status_code == 200

    result = self.client.get('/login')
    assert result.status_code == 302

  def test_invalid_login(self):
    """
    Should get status code 401
    """
    result = self.client.post('/login', data=dict(
      username='user1',
      password='user111'
    ), follow_redirects=True)

    assert result.status_code == 401

  def test_user_logged_in_logout(self):
    """
    Should redirect if the user is logged in and press logout
    status code should be 302
    """
    result = self.client.post('/login', data=dict(
      username='user1',
      password='user1'
    ), follow_redirects=True)
    assert b'user1 Logout' in result.data
    assert result.status_code == 200

    result = self.client.get('/logout')
    assert result.status_code == 302  

class TestError404Route(TestMainRoute):

  def test_404_error(self):
    """
    Should get status code 404
    """
    result = self.client.post('/login', data=dict(
      username='user1',
      password='user1'
    ), follow_redirects=True)

    result = self.client.put('/unknown-enpoint')

    assert b'Resource Not Found' in result.data
    assert result.status_code == 404


class TestErrorCSRFRoute(TestMainRoute):

  def setUp(self):
    self.client = app_protected.test_client()

  def test_CSRF_error(self):
    """
    The CSRF token Should be missing
    """
    result = self.client.post('/login', data=dict(
      username='user1',
      password='user1'
    ), follow_redirects=True)

    assert b'The CSRF token is missing.' in result.data
    assert result.status_code == 400


class TestTodoRoute(TestMainRoute):

  def login_user(self):
    return  self.client.post('/login', data=dict(
      username='user1',
      password='user1'
    ), follow_redirects=True)

  def test_todo_available(self):
    """
    Should exist in the returned page a ToDo with description
      - Ad laborum ea culpa cupidatat commodo do.
    """
    result = self.login_user()
    result = self.client.get('/todo/1')

    assert b'Ad laborum ea culpa cupidatat commodo do.' in result.data
    assert result.status_code == 200

  def test_todo_not_found(self):
    """
    Should not exist a ToDo with id 20, the returned page should have
      - Resource Not Found
    """
    result = self.login_user()
    result = self.client.get('/todo/20', follow_redirects=True)

    assert b'Resource Not Found' in result.data
    assert result.status_code == 404

  def test_list_todo(self):
    """
    The first 5 user1 ToDo should exist on the page
    """
    result = self.login_user()
    result = self.client.get('/todo?page=1')

    todos = Todo.query.filter_by(user_id=1).order_by(Todo.id.desc()).paginate(page=1, per_page=5)
    for todo in todos.items:
      assert todo.description.encode() in result.data
    assert result.status_code == 200

  def test_post_todo(self):
    """
    After a ToDo is created should appear in the returned page
    """
    result = self.login_user()
    result = self.client.post('/todo', data=dict(
      description='My First ToDo'
    ), follow_redirects=True)

    assert result.status_code == 200
    assert b'My First ToDo' in result.data

  def test_post_todo_with_empty_description(self):
    """
    If the user try to create a ToDo with an empty description the
    returned page should have 'Description can not be empty'
    """
    result = self.login_user()
    result = self.client.post('/todo', data=dict(
      description=''
    ), follow_redirects=True)

    assert b'Description can not be empty' in result.data
    assert result.status_code == 200

  def test_post_todo_with_white_spaces_description(self):
    """
    If the user try to create a ToDo with white spaces in description the
    returned page should have 'Description can not be only white space'
    """
    result = self.login_user()
    result = self.client.post('/todo', data=dict(
      description='    '
    ), follow_redirects=True)

    assert b'Description can not be only white space' in result.data
    assert result.status_code == 200

  def test_delete_todo(self):
    """
    After delete the first a ToDo the user should get a feedback
    'ToDo deleted!'
    """
    result = self.login_user()
    result = self.client.delete('/todo/1')

    assert b'ToDo deleted!' in result.data
    assert result.status_code == 200

  def test_completed_todo(self):
    """
    After complete the first a ToDo the user should get a feedback
    'ToDo Ready!'
    """
    result = self.login_user()
    result = self.client.put('/todo/2/complete')

    assert b'ToDo Ready!' in result.data
    assert result.status_code == 200

  def test_get_json_todo(self):
    """
    The endpoint's(json) response must be
    - {\n  "completed": false, \n  "description": "Consectetur dolore proident aliqua qui minim.", \n  "id": 2, \n  "user_id": 1\n}\n
    """
    result = self.login_user()
    result = self.client.get('/todo/2/json')

    assert b'{\n  "completed": false, \n  "description": "Consectetur dolore proident aliqua qui minim.", \n  "id": 2, \n  "user_id": 1\n}\n' in result.data
    assert result.status_code == 200

  def test_todo_not_available(self):
    """
    A ToDo is not found if does not exist or belong to
    other user.

    If the ToDo does not exists, the feedback must be
    'Oops, ToDo not found!'
    """
    result = self.login_user()

    # not exist
    result = self.client.delete('/todo/30')
    assert b'Oops, ToDo not found!' in result.data
    assert result.status_code == 404

    result = self.client.put('/todo/30/complete')
    assert b'Oops, ToDo not found!' in result.data
    assert result.status_code == 404

    result = self.client.get('/todo/30/json')
    assert b'Oops, ToDo not found!' in result.data
    assert result.status_code == 404

    # belong to user2
    result = self.client.delete('/todo/8')
    assert b'Oops, ToDo not found!' in result.data
    assert result.status_code == 404

  def test_todo_options_user_not_logged(self):
    """
    If the user is not logged, the actions
    - delete
    - complete
    - json
    Must be get 'To perform this action you must be logged in!'
    """

    result = self.client.delete('/todo/1')
    assert b'To perform this action you must be logged in!' in result.data
    assert result.status_code == 401

    result = self.client.put('/todo/2/complete')
    assert b'To perform this action you must be logged in!' in result.data
    assert result.status_code == 401

    result = self.client.get('/todo/2/json')
    assert b'To perform this action you must be logged in!' in result.data
    assert result.status_code == 401

  