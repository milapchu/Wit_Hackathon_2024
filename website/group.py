from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website import db 
from .models import Task, Group 

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
            new_group = Group(group_name=group_name)
            new_group.members.append(current_user)
            current_user.group_name = group_name
            db.session.add(new_group)
            db.session.commit()

            flash('Group created successfully!', category='success')
            return redirect(url_for('views.group'))

    
    return render_template("create_group.html", user=current_user)

@group.route('/join_group', methods=['GET', 'POST'])
@login_required
def join_group():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        
        # Check if the user is already in a group
        if current_user.group:
            flash('You are already a member of a group.', category='error')
            return redirect(url_for('views.group'))

        # Find the group by name
        group = Group.query.filter_by(group_name=group_name).first()
        
        if not group:
            flash('Group not found.', category='error')
            return redirect(url_for('group.join_group'))  # Redirect to the same page for the user to try again
        else:
            # Add user to the group
            current_user.group = group
            db.session.commit()

            flash('You have joined the group successfully!', category='success')
            return redirect(url_for('views.group'))

    return render_template("join_group.html", user=current_user)  # Ensure you have a return for GET requests


