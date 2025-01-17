from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from unittest import skip
from user_app.models import CustomUser


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('registration')

    def test_registration(self):
        data = {
            "username" : "test",
            "email" : "test@test.de",
            "password" : "test",
            "repeated_password" : "test",
            "type" : "customer"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("user_id", response.data)

    def test_passwords_dont_match(self):
        data = {
            "username" : "test",
            "email" : "test@test.de",
            "password" : "password123",
            "repeated_password" : "password456",
            "type" : "customer"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("user_id", response.data)

    def test_register_customer(self):
        data = {
            "username" : "customer",
            "email" : "customer@customer.de",
            "password" : "password123",
            "repeated_password" : "password123",
            "type" : "customer"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user_id", response.data)

    def test_register_business(self):
        data = {
            "username": "business",
            "email": "business@business.de",
            "password": "password123",
            "repeated_password": "password123",
            "type": "business"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user_id", response.data)

    def test_duplicate_username(self):
        CustomUser.objects.create_user(
            username="test",
            email="test1@test.de",
            password="test123"
        )

        data = {
            "username": "test",
            "email": "newtest@test.de",
            "password": "test",
            "repeated_password": "test",
            "type": "customer",
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_duplicate_email(self):
        CustomUser.objects.create_user(
            username="newuser",
            email="test@test.de",
            password="test123"
        )

        data = {
            "username": "newtest",
            "email": "test@test.de",
            "password": "test",
            "repeated_password": "test",
            "type": "customer",
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)