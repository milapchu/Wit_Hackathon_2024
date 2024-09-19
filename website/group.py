
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website import db 
from .models import Task, Group , user_group

group = Blueprint('group', __name__)

@group.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        group_name = request.form.get('group_name')

        group = Group.query.filter_by(group_name=group_name).first()

        if group: #Group name already exists, choose another one
            flash('Group Name already exists', category='error')
        
        else:
            flash('Create group!')
            new_group = Group(
                group_name=group_name
            )
            db.session.add(new_group)
            db.session.commit()
            return redirect(url_for('views.group'))

    
    return render_template("create_group.html", user=current_user)

@group.route('/join_group', methods=['GET', 'POST'])
@login_required
def join_group():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        
        group = Group.query.filter_by(group_name=group_name).first()
        
        if group:
            is_member = db.session.execute(
                db.select(user_group).where(
                    (user_group.c.user_id == current_user.id) &
                    (user_group.c.group_id == group.id)
                )
            ).fetchone()
            
            if is_member:
                existing_task = Task.query.filter_by(user_id=current_user.id, group_id=group.id).first()
                
                if existing_task:
                    flash('You are already in the group. Try to add more tasks!', category='error')
                else:
                    flash('You are in the group, let us have some tasks!', category='success')
                
                return redirect(url_for('task.create_task'))
            else:
                current_user.groups.append(group)
                db.session.commit()
                flash('You have successfully joined the group!', category='success')
                return redirect(url_for('task.create_task'))
        else:
            flash('Group does not exist. Please enter a valid group name.', category='error')
            return redirect(url_for('group.join_group'))
    
    # For GET requests, render the join group page
    return render_template('join_group.html', user=current_user)

