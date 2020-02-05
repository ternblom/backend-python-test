from flask import g, render_template, request, session, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user
from alayatodo.models import User, UserSchema
from alayatodo._auth import bp


@bp.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('_todo.todos'))
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
      login_user(user)
      next_page = request.args.get('next')
      flash('You have been logged in!', 'success')
      return redirect(next_page) if next_page else redirect(url_for('_todo.todos'))
    else:
      flash('Login Unsuccessful. Please check username and password.', 'danger')

    return render_template('login.html'), 401

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('_main.home'))