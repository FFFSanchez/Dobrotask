from http import HTTPStatus

from django.test import Client, TestCase
from rest_framework.test import APIClient

from users.models import User


class TasksAPITestCase(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.auth_client = APIClient()
        user = User.objects.create("fff", "fff@fff.ru")

        self.auth_client.force_authenticate(user=user)

    def test_register(self):
        """ Create user """

        data = {
            'username': 'fff2',
            'email': 'fff2@fff.ru',
            'password': 'asf32fdasd'
        }
        response = self.guest_client.post('/api/auth/users/', data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_guest_get_tasks(self):
        """ Guest get 401 """

        response = self.guest_client.get('/api/tasks/my_tasks_to_do/')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_make_task(self):
        """ Create task """

        data = {
            "title": "task1",
            "description": "desc1"
        }
        response = self.auth_client.post('/api/tasks/', data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_get_my_tasks(self):
        """ Get authed tasks """

        response = self.auth_client.get('/api/tasks/my_tasks_created_by_me/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
