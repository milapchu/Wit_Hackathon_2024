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
            new_group = Group(
                group_name=group_name
            )
            db.session.add(new_group)
            db.session.commit()
            return redirect(url_for('views.group'))

    
    return render_template("create_group.html", user=current_user)


