from flask import Blueprint, render_template
from website import db
from .models import User, Group, user_group, Task
from flask_login import current_user
from datetime import datetime, timedelta

#@??.route('/')
def group_members():
    query = """
    SELECT
        ug.group_id
        g.group_name,
        u.first_name
    FROM
        user_group ug
    JOIN
        "Group" g ON ug.group_id = g.id
    JOIN
        "User" u ON ug.user_id = u.id
    ORDER BY
        g.group_name, u.first_name;
    """
    group_user = db.session.execute(query).fetchall()
    
    return group_user
# get the group_id via current_user's group as well
#put all those 3 methods inside def get_all_allo()

def list_of_task():
    list_tasks = db.session.query(
        Task.group_id,
        Group.group_name,
        Task.task_name,
        Task.frequency,
        Task.status,
        Task.date
    ).join(
        Task, Group.id == Task.group_id
    ).filter(
        Task.status == 'Not Done'
    ).order_by(
        Group.group_name, Task.date
    ).all()
    return list_tasks



def get_id():
    current_group = current_user.groups
    return current_group.id


def get_all_allo():
    group_user = group_members()  
    list_tasks = list_tasks()  
    current_group_ids = [group.id for group in get_id()]  
    filtered_tasks = [
        task for task in list_tasks 
        if task.group_id in current_group_ids
    ]
    
    allocated_tasks = []
    end_date = datetime(2025, 1, 1)

    for task in filtered_tasks:
        group_name = task.group_name
        task_name = task.task_name
        frequency = task.frequency
        task_date = task.date

        if frequency == 'Daily':
            next_date = task_date + timedelta(days=1)
        elif frequency == 'Weekly':
            next_date = task_date + timedelta(weeks=1)
        elif frequency == 'Fortnightly':
            next_date = task_date + timedelta(weeks=2)
        elif frequency == 'Monthly':
            next_date = task_date + timedelta(weeks=4)
        else:
            next_date = task_date
        
        # Stop assigning tasks if the next_date exceeds the end_date
        if next_date > end_date:
            continue
        
        users_in_group = [user.first_name for user in group_user if user.group_name == group_name]

        # Assign tasks to users
        for user_name in users_in_group:
            allocated_tasks.append({
                'Task Name': task_name,
                'Date': next_date.strftime('%Y-%m-%d'),
                'Group Name': group_name,
                'User Name': user_name
            })
    
    return allocated_tasks


