from flask import render_template, request, redirect, flash, abort, url_for, current_app as app, make_response
from flask_login import current_user, login_required
from alayatodo import db
from alayatodo.models import User, Todo, TodoSchema
from alayatodo.helpers import get_pagination_info
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
    page, per_page, todo_filter_by = get_pagination_info()

    filters = {'user':current_user, 'completed': True} if todo_filter_by == 'completed' else {'user':current_user}
    todos = Todo.query.filter_by(**filters).order_by(Todo.completed.asc(), Todo.id.desc()).paginate(page=page, per_page=per_page, error_out=False)

    resp = make_response(render_template(
        'todo/todos.html', 
        todos=todos, 
        page=page, 
        per_page=per_page, 
        per_page_list=app.config['TODOS_PER_PAGE_LIST'],
        todo_filter_by=todo_filter_by
    ))
    resp.set_cookie('TODOS_PER_PAGE', str(per_page))
    resp.set_cookie('TODOS_ACTIVE_PAGE', str(page))
    resp.set_cookie('TODOS_FILTER_BY', str(todo_filter_by))
    return resp
    


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
        todo.completed = request.form.get('complete') == "1"
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
    