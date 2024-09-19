from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website import db
from .models import Task, Group, TaskFrequency

task = Blueprint('task', __name__)

@task.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        task_name = request.form.get('task')
        frequency = request.form.get('frequency')
        group_name = request.form.get('group_name')

        group = Group.query.filter_by(group_name=group_name).first()

        # Check if the frequency is a valid TaskFrequency member
        if frequency in TaskFrequency.__members__:
            frequency_enum = TaskFrequency[frequency]
        else:
            flash('Invalid task frequency! Please choose from Daily, Weekly, Fortnightly, or Monthly.', category='error')
            return redirect(url_for('task.create_task'))
                            
        if group:
            flash('Task added!', category='success')
            new_task = Task(
                task_name=task_name, 
                user_id=current_user.id, 
                frequency=frequency_enum, 
                group_id=group.id
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('task.create_task'))
        else:
            flash('Group id does not exist, please insert again', category='error')

    return render_template("create_task.html", user=current_user)

@task.route('/view_tasks', methods=['GET'])
@login_required
def view_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    print(current_user.id)
    return render_template('view_tasks.html', tasks=tasks, user=current_user)

@task.route('/allocate_tasks', methods=['GET', 'POST'])
@login_required
def allocate_tasks():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        frequency = request.form.get('frequency')

        group = Group.query.filter_by(group_name=group_name).first()

        if group:
            allocate_tasks_randomly(group_id=group.id, frequency=frequency)
            flash('Tasks have been allocated successfully!', category='success')
        else:
            flash('Group name does not exist. Please enter a valid group name.', category='error')

    return render_template('task_allocation.html', user=current_user)

def allocate_tasks_randomly(group_id, frequency):
    pass
