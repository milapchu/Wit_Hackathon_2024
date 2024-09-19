from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import random
from datetime import datetime, timedelta

task = Blueprint('task', __name__)

@task.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    from website import db
    from .models import Task, Group
    if request.method == 'POST':
        task_name = request.form.get('task')
        frequency = request.form.get('frequency')
        
        user_group = current_user.group
        group_name = user_group.group_name

        # Define allowed frequency values
        allowed_frequencies = ['Daily', 'Weekly', 'Fortnightly', 'Monthly']

        frequency_normalize = frequency.capitalize()

        # Check if the frequency is valid
        if frequency_normalize not in allowed_frequencies:
            flash('Invalid task frequency! Please choose from Daily, Weekly, Fortnightly, or Monthly.', category='error')
            return redirect(url_for('task.create_task'))
        
        group = Group.query.filter_by(group_name=group_name).first()

        if group:
            flash('Task added!', category='success')
            new_task = Task(
                task_name=task_name,  
                frequency=frequency_normalize,
                group_id=group.id
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('task.create_task'))
        else:
            flash('Group name does not exist, please insert again', category='error')

    return render_template("create_task.html", user=current_user)

@task.route('/view_tasks', methods=['GET'])
@login_required
def view_tasks():
    from website import db
    from .models import Task
    
    if not current_user.group:
        flash('You are not in any group.', category='error')
        return redirect(url_for('some_other_view'))  # Redirect to an appropriate view

    # Retrieve only the tasks assigned to the current user in their group
    tasks = Task.query.filter_by(group_id=current_user.group.id, user_id=current_user.id).all()

    return render_template('view_tasks.html', tasks=tasks, user=current_user)

def allocate_tasks_randomly(group_id, frequency):
    from website import db
    from .models import Task, Group, User

    group = Group.query.filter_by(id=group_id).first()
    if not group:
        print(f"No group found with id {group_id}")
        return
    
    # Fetch users in the group using the association table
    group_users = group.members
    print(f"Group Users: {[user.first_name for user in group_users]}")
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
        if task.frequency == 'Weekly':
            next_allocation = task.last_allocated + timedelta(weeks=1)
        elif task.frequency == 'Daily':
            next_allocation = task.last_allocated + timedelta(days=1)
        elif task.frequency == 'Monthly':
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
        user_group_id = current_user.group.id
        frequency = request.form.get('frequency')
        action = request.form.get('action')
        
        group = Group.query.get(user_group_id)

        if user_group_id:
            # Call the task allocation function
            allocate_tasks_randomly(group_id=user_group_id, frequency=frequency)

            if action == 'view_allocated':
                allocated_tasks = Task.query.filter_by(group_id=user_group_id, user_id=current_user.id).all()
                return render_template('view_tasks.html', tasks=allocated_tasks, user=current_user)
            elif action == 'view_all':
                all_tasks = Task.query.filter_by(group_id=user_group_id).all()
                return render_template('view_all_tasks.html', tasks=all_tasks, group=group, user=current_user)
        else:
            flash('You have not been in any group, please create or join one', category='error')

    return render_template('task_allocation.html', user=current_user)