from alayatodo._todo import bp
from flask import g, render_template, request, session, redirect


@bp.route('/todo/<id>', methods=['GET'])
def todo(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)


@bp.route('/todo', methods=['GET'])
@bp.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    return render_template('todos.html', todos=todos)


@bp.route('/todo', methods=['POST'])
@bp.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute(
        "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
        % (session['user']['id'], request.form.get('description', ''))
    )
    g.db.commit()
    return redirect('/todo')


@bp.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    return redirect('/todo')