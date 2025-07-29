from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(user=self.user, title='Test Task', description='Test Desc')

    def test_task_str(self):
        self.assertEqual(str(self.task), 'Test Task')

    def test_task_defaults(self):
        self.assertFalse(self.task.complete)
        self.assertIsNotNone(self.task.created)

class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_task_list_view(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_task_create_view(self):
        response = self.client.post('/tasks/create/', {'title': 'New Task', 'description': 'Desc', 'complete': False})
        self.assertEqual(response.status_code, 302)  # Redirect after creation