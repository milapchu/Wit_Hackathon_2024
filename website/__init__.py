from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

db = SQLAlchemy()
DB_NAME = "database.db"

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

    # Initialize the database
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

    from .task import allocate_tasks_by_frequency

    # Set up APScheduler for task allocation
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=allocate_tasks_by_frequency, trigger="interval", hours=24)  # Runs every 24 hours
    scheduler.start()

    # Shut down the scheduler when the app exits
    atexit.register(lambda: scheduler.shutdown())

    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
