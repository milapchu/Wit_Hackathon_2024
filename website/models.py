from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Enum
from datetime import datetime



# # Association table to link users and groups (many-to-many relationship)
# user_group = db.Table(
#     'user_group',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
# )

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(Enum('Done', 'Not Done', name='task_status'), nullable=False, default='Not Done')
    frequency = db.Column(Enum('Daily', 'Weekly', 'Fortnightly', 'Monthly', name='task_frequency'), nullable=False)
    last_allocated = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # one user can have many tasks
    group_id  = db.Column(db.Integer, db.ForeignKey('group.id')) # one group can have many tasks
    user = db.relationship('User', back_populates='tasks')
    group = db.relationship('Group', back_populates='tasks')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    # groups = db.relationship('Group', secondary=user_group, backref=db.backref('members', lazy=True)) # Many-to-many with groups
    tasks = db.relationship('Task', back_populates='user') #all tasks of a user
    group = db.relationship('Group', back_populates='members')

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name  = db.Column(db.String(100), nullable=False, unique=True)
    tasks = db.relationship('Task', back_populates='group') #all tasks of a user
    members = db.relationship('User', back_populates='group')

