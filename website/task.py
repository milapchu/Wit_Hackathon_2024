from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website import db
from .models import Task, Group

task = Blueprint('task', __name__)

@task.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        task_name = request.form.get('task')
        frequency = request.form.get('frequency')
        group_id = request.form.get('group_id')

        group = Group.query.filter_by(id=group_id).first()
        if group:
            flash('Added task to your group successfully', category='success')
            new_task = Task(
                task_name=task_name, 
                user_id=current_user.id, 
                frequency=frequency, 
                group_id=group_id
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('task.create_task'))
        else:
            flash('Group id does not exist, please insert again', category='error')

    return render_template("create_task.html", user=current_user)
