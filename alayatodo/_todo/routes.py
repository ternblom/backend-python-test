from flask import g, render_template, request, session, redirect, flash
from flask_apispec import marshal_with
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
    try:
        user = User.query.get_or_404(session['user']['id'])
        todo = Todo(description=request.form.get('description'), user=user)
        db.session.add(todo)
        db.session.commit()
        flash('Your todo has been created!', 'success')
    except AssertionError as err:
        flash(err.args[0], 'danger')
        db.session.rollback()
    return redirect('/todo')


@bp.route('/todo/<id>', methods=['DELETE'])
def todo_delete(id):
    if not session.get('logged_in'):
        return ('To perform this action you must be logged!', 401)
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return 'ToDo deleted!'
    return ('Oops, ToDo not found!', 404)

@bp.route('/todo/<id>/complete', methods=['PUT'])
def todo_complete(id):
    if not session.get('logged_in'):
        return ('To perform this action you must be logged!', 401)
    todo = Todo.query.get(id)
    if todo:
        todo.completed = True
        db.session.commit()
        return 'ToDo Ready!'
    return ('Oops, ToDo not found!', 404)