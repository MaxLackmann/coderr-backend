from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token
from user_app.models import CustomUser
from unittest import skip


class LoginTestCase(APITestCase):
    def setUp(self):
        self.customer = CustomUser.objects.create_user(
            username='testcustomer',
            email='testcustomer@test.de',
            password='password123',
            type='customer'
        )
        
        self.business = CustomUser.objects.create_user(
            username='testbusiness',
            email='testbusiness@test.de',
            password='password123',
            type='business'
        )
        self.client = APIClient()
        self.login_url = reverse('login')

    def test_login_customer(self):
        data = {
            'username': 'testcustomer',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testcustomer')
        self.assertEqual(response.data['user_id'], self.customer.id)

    def test_login_business(self):
        data = {
            'username': 'testbusiness',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testbusiness')
        self.assertEqual(response.data['user_id'], self.business.id)

    def test_invalid_username(self):
        data = {
            'username': 'wronguser',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_password(self):
        data = {
            'username': 'testcustomer',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'username': 'testbusiness',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)