from rest_framework.test import APITestCase
from rest_framework import status
from user_app.models import CustomUser, GuestToken
from django.utils.timezone import now, timedelta
from django.urls import reverse
from rest_framework.test import APIClient

class GuestLoginTestCase(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.client = APIClient()

        self.guest_customer = {"username": "andrey", "password": "asdasd"}
        self.guest_business = {"username": "kevin", "password": "asdasd24"}

    def test_guest_customer_login_creates_token(self):
        response = self.client.post(self.login_url, self.guest_customer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

        user = CustomUser.objects.get(username="andrey")
        self.assertTrue(GuestToken.objects.filter(user=user).exists())

    def test_guest_business_login_creates_token(self):
        response = self.client.post(self.login_url, self.guest_business)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

        user = CustomUser.objects.get(username="kevin")
        self.assertTrue(GuestToken.objects.filter(user=user).exists())

    def test_guest_token_expires(self):
        response = self.client.post(self.login_url, self.guest_customer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = CustomUser.objects.get(username="andrey")

        GuestToken.objects.filter(user=user).update(created=now() - timedelta(hours=2))

        expired_tokens = GuestToken.objects.filter(user=user, created__lt=now() - timedelta(hours=2))
        self.assertTrue(expired_tokens.exists())

    def test_guest_login_deletes_expired_tokens(self):
        response = self.client.post(self.login_url, self.guest_customer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = CustomUser.objects.get(username="andrey")

        GuestToken.objects.filter(user=user).update(created=now() - timedelta(hours=2))

        response = self.client.post(self.login_url, self.guest_customer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(GuestToken.objects.filter(user=user).count(), 1)