from flask import g, render_template, request, session, redirect
from alayatodo.models import User, UserSchema
from alayatodo._auth import bp


@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username, password=password).first_or_404()

    if user:
        user_schema = UserSchema()
        session['user'] = dict(user_schema.dump(user))
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')

@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')