from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token
from user_app.models import CustomUser
from unittest import skip

class ProfileTestCase(APITestCase):
    def setUp(self):
        self.customer = CustomUser.objects.create_user(
            username='testcustomer',
            email='testcustomer@test.de',
            password='password123',
            type='customer'
        )
        
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.profile_url = reverse('profile', kwargs={'user_id': self.customer.id})