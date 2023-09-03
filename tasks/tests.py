from http import HTTPStatus

from django.test import Client, TestCase


class RefsAPITestCase(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_register(self):
        """ Smoke check """

        data = {
            'username': 'fff',
            'email': 'fff@fff.ru',
            'password': 'asf32fdasd'
        }
        response = self.guest_client.post('/api/auth/users/', data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
