from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from .models import User, Group, Task
from .task import allocate_tasks_randomly
import atexit
from datetime import datetime, timedelta

db = SQLAlchemy()
DB_NAME = "database.db"

def allocate_tasks_by_frequency():
    with scheduler.app.app_context():
        # Get current time and calculate the time for the next allocation
        now = datetime.now()

        # Get all the tasks from the database
        tasks = Task.query.all()

        # Iterate through each task and allocate based on the frequency
        for task in tasks:
            if task.frequency == 'WEEKLY':
                # Check if it's been a week since the last allocation
                next_allocation = task.last_allocated + timedelta(weeks=1)
                if now >= next_allocation:
                    allocate_tasks_randomly(task.group_id, task.frequency)
                    task.last_allocated = now  # Update the last allocation time
                    db.session.commit()
            elif task.frequency == 'DAILY':
                next_allocation = task.last_allocated + timedelta(days=1)
                if now >= next_allocation:
                    allocate_tasks_randomly(task.group_id, task.frequency)
                    task.last_allocated = now
                    db.session.commit()
            elif task.frequency == 'MONTHLY':
                next_allocation = task.last_allocated + timedelta(days=30)  # Approximate month
                if now >= next_allocation:
                    allocate_tasks_randomly(task.group_id, task.frequency)
                    task.last_allocated = now
                    db.session.commit()

def create_scheduler(app):
    global scheduler  # Declare scheduler as global to be accessible in allocate_tasks_by_frequency
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=allocate_tasks_by_frequency, trigger="interval", hours=1)
    scheduler.start()

    # Shut down the scheduler when the app exits
    atexit.register(lambda: scheduler.shutdown())

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'BFAJBFAJDBCDABCIUDAKBCDBCJHAB'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
     # Register blueprints for routing
    from .views import views
    from .auth import auth
    from .task import task
    from .group import group

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(task, url_prefix='/task')
    app.register_blueprint(group, url_prefix='/group')



    from .models import User, Group, Task
    
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get((int(id)))
    
    # Debug route
    @app.route('/debug-url')
    def debug_url():
        try:
            return str(url_for('task.create_task'))
        except Exception as e:
            return str(e)


    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


