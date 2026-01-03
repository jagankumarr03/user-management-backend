from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class AuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_login(self):
        response = self.client.post("/api/token/", {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, 200)
