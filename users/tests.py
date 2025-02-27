from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import CustomUser

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'password123'
        }

    def test_user_registration(self):
        response = self.client.post(reverse('user-register'), self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(CustomUser.objects.filter(email='test@example.com').exists())