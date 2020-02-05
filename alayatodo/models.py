from flask_login import UserMixin
from sqlalchemy.orm import validates
from alayatodo import db, ma, bcrypt, login_manager


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  todos = db.relationship('Todo', backref='user', lazy=True)

  def __repr__(self):
    return f"User('{self.username}')"

  def set_password(self, password):
    self.password = bcrypt.generate_password_hash(password).decode('utf8')

  def check_password(self, password):
    return bcrypt.check_password_hash(self.password, password)


class Todo(db.Model):
  __tablename__ = "todos"
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  completed = db.Column(db.Boolean, default=False)

  def __repr__(self):
    return f"Todo('{self.description}')"

  @validates('description')
  def validate_description(self, key, value):
    assert not value.isspace(), 'Description can not be only white space.'
    assert value != "", 'Description can not be empty.'
    return value


class UserSchema(ma.ModelSchema):
  class Meta:
      model = User
      fields = ('id', 'username')

      
class TodoSchema(ma.ModelSchema):
  class Meta:
      model = User
      fields = ('id', 'description', 'completed', 'user_id')
