from flask import g, render_template, request, session, redirect
from alayatodo import db
from alayatodo.models import User, Todo, TodoSchema
from alayatodo._todo import bp


@bp.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todo.query.get_or_404(id)
    return render_template('todo.html', todo=todo)


@bp.route('/todo', methods=['GET'])
@bp.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    todos = Todo.query.all()
    return render_template('todos.html', todos=todos)


@bp.route('/todo', methods=['POST'])
@bp.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    user = User.query.get_or_404(session['user']['id'])
    todo = Todo(description=request.form.get('description', ''), user=user)
    db.session.add(todo)
    db.session.commit()

    return redirect('/todo')


@bp.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todo')