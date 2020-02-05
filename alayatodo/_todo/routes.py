from flask import render_template, request, session, redirect, flash, abort, url_for
from flask_login import current_user, login_required
from alayatodo import db
from alayatodo.models import User, Todo, TodoSchema
from alayatodo._todo import bp


@bp.route('/todo/<id>', methods=['GET'])
@login_required
def todo(id):
    todo = Todo.query.filter_by(user=current_user, id=id).first()
    if todo:
        return render_template('todo/todo.html', todo=todo)
    abort(404)


@bp.route('/todo', methods=['GET'])
@login_required
def todos():
    page = request.args.get('page', 1, type=int)
    todos = Todo.query.filter_by(user=current_user).order_by(Todo.id.desc()).paginate(page=page, per_page=5)
    return render_template('todo/todos.html', todos=todos)


@bp.route('/todo', methods=['POST'])
@login_required
def todos_POST():
    try:
        todo = Todo(description=request.form.get('description'), user=current_user)
        db.session.add(todo)
        db.session.commit()
        flash('Your todo has been created!', 'success')
    except AssertionError as err:
        flash(err.args[0], 'danger')
        db.session.rollback()
    return redirect(url_for('_todo.todos'))


@bp.route('/todo/<id>', methods=['DELETE'])
def todo_delete(id):
    if not current_user.is_authenticated:
        return ('To perform this action you must be logged in!', 401)
    todo = Todo.query.filter_by(user=current_user, id=id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return 'ToDo deleted!'
    return ('Oops, ToDo not found!', 404)


@bp.route('/todo/<id>/complete', methods=['PUT'])
def todo_complete(id):
    if not current_user.is_authenticated:
        return ('To perform this action you must be logged in!', 401)
    todo = Todo.query.filter_by(user=current_user, id=id).first()
    if todo:
        todo.completed = True
        db.session.commit()
        return 'ToDo Ready!'
    return ('Oops, ToDo not found!', 404)


@bp.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not current_user.is_authenticated:
        return ('To perform this action you must be logged in!', 401)
    todo = Todo.query.filter_by(user=current_user, id=id).first()
    if todo:
        todo_schema = TodoSchema()
        return todo_schema.dump(todo)
    return ('Oops, ToDo not found!', 404)
    