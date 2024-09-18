from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
#new 
from models import Task

auth = Blueprint('auth', __name__)

@auth.route('/create-task', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        frequency = request.form.get('task_frenquency')
        if len(task_name) < 1:
            flash('Task name is too short!',category='error')
        else:
            new_task = Task(task_name=task_name, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task created successfully!', category='success')
            return redirect(url_for('auth.create'))

    return render_template("create.html", user=current_user)



