from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import random
from datetime import datetime, timedelta

task = Blueprint('task', __name__)

@task.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    from website import db
    from .models import Task, Group, user_group, TaskFrequency, TaskStatus
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
    from website import db
    from .models import Task
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('view_tasks.html', tasks=tasks, user=current_user)

def allocate_tasks_randomly(group_id, frequency):
    from website import db
    from .models import Task, Group, User, user_group

    group = Group.query.filter_by(id=group_id).first()
    if not group:
        print(f"No group found with id {group_id}")
        return
    
    # Fetch users in the group using the association table
    group_users = User.query.join(user_group).filter(user_group.c.group_id == group_id).all()
    if not group_users:
        print(f"No users found in group with id {group_id}")
        return
    
    tasks = Task.query.filter_by(group_id=group_id, frequency=frequency).all()
    if not tasks:
        print(f"No tasks found in group {group_id} with frequency {frequency}")
        return

    random.shuffle(group_users)

    for index, task in enumerate(tasks):
        assigned_user = group_users[index % len(group_users)]
        task.user_id = assigned_user.id
        print(f"Task '{task.task_name}' assigned to user '{assigned_user.first_name}'")
    
    db.session.commit()
    print("Tasks have been successfully allocated.")

def allocate_tasks_by_frequency():
    from website import db
    from .models import Task

    now = datetime.now()
    tasks = db.session.query(Task).all()
    for task in tasks:
        if task.frequency == 'WEEKLY':
            next_allocation = task.last_allocated + timedelta(weeks=1)
        elif task.frequency == 'DAILY':
            next_allocation = task.last_allocated + timedelta(days=1)
        elif task.frequency == 'MONTHLY':
            next_allocation = task.last_allocated + timedelta(days=30)
        else:
            continue  # Skip if frequency is not recognized

        if now >= next_allocation:
            allocate_tasks_randomly(task.group_id, task.frequency)
            task.last_allocated = now
            db.session.commit()

@task.route('/allocate_tasks', methods=['GET', 'POST'])
@login_required
def allocate_tasks():
    from website import db
    from .models import Task, Group
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        frequency = request.form.get('frequency')

        group = Group.query.filter_by(group_name=group_name).first()

        if group:
            # Call the task allocation function
            allocate_tasks_randomly(group_id=group.id, frequency=frequency)

            # Retrieve the allocated tasks after the allocation is done
            allocated_tasks = Task.query.filter_by(group_id=group.id, frequency=frequency).all()

            flash('Tasks have been allocated successfully!', category='success')

            # Pass the allocated tasks to the new template
            return render_template('view_allocated_tasks.html', tasks=allocated_tasks, group=group, user=current_user)
        else:
            flash('Group name does not exist. Please enter a valid group name.', category='error')

    return render_template('task_allocation.html', user=current_user)
