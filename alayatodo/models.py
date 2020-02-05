from alayatodo import db, ma


class User(db.Model):
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

  def __repr__(self):
    return f"Todo('{self.description}')"


class UserSchema(ma.ModelSchema):
  class Meta:
      model = User
      fields = ('id', 'username')

      
class TodoSchema(ma.ModelSchema):
  class Meta:
      model = User
      fields = ('id', 'description', 'user_id')
