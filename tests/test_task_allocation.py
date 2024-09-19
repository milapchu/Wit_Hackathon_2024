import unittest
from website import create_app, db
from website.models import Task, Group, User, user_group
from datetime import datetime, timedelta

class TestTaskAllocation(unittest.TestCase):
    def setUp(self):
        app = create_app('testing')
        self.client = app.test_client()
        app_context = app.app_context()
        app_context.push()
        db.create_all()

        # Setup test data
        self.group = Group(group_name='Test Group')
        db.session.add(self.group)
        db.session.commit()
        self.users = [User(email=f'user{i}@example.com', password='password', first_name=f'User{i}') for i in range(3)]
        db.session.add_all(self.users)
        db.session.commit()
        self.tasks = [Task(task_name=f'Task{i}', frequency='Daily', group_id=self.group.id) for i in range(5)]
        db.session.add_all(self.tasks)
        db.session.commit()

    def test_allocate_tasks_randomly(self):
        from website.task import allocate_tasks_randomly
        allocate_tasks_randomly(self.group.id, 'Daily')
        tasks = Task.query.filter_by(group_id=self.group.id).all()
        self.assertTrue(all(task.user_id is not None for task in tasks))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
