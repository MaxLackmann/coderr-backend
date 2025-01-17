from rest_framework.test import APITestCase
from rest_framework import status
from user_app.models import CustomUser, GuestToken
from django.utils.timezone import now, timedelta
from django.urls import reverse

class GuestLoginTestCase(APITestCase):
    """Testet den Guest-Login-Flow"""

    def setUp(self):
        """Vorbereitung für Tests"""
        self.login_url = reverse('login')  # Klarer Name für die Login-URL

        # Vordefinierte Guest-Logindaten (sollten mit `GUEST_USERS` in LoginSerializer übereinstimmen)
        self.guest_customer = {"username": "andrey", "password": "asdasd"}
        self.guest_business = {"username": "kevin", "password": "asdasd24"}

    def test_guest_customer_login_creates_token(self):
        """Testet, ob ein Guest-Token für `andrey` erstellt wird"""
        response = self.client.post(self.login_url, self.guest_customer)  # Nutzung von `self.login_url`

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

        # Überprüfen, ob ein GuestToken in der DB existiert
        user = CustomUser.objects.get(username="andrey")
        self.assertTrue(GuestToken.objects.filter(user=user).exists())

    def test_guest_business_login_creates_token(self):
        """Testet, ob ein Guest-Token für `kevin` erstellt wird"""
        response = self.client.post(self.login_url, self.guest_business)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

        user = CustomUser.objects.get(username="kevin")
        self.assertTrue(GuestToken.objects.filter(user=user).exists())

    def test_guest_token_expires(self):
        """Testet, ob ein Guest-Token nach Ablauf nicht mehr gültig ist"""
        response = self.client.post(self.login_url, self.guest_customer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = CustomUser.objects.get(username="andrey")
        guest_token = GuestToken.objects.filter(user=user).first()

        # Ablaufzeit künstlich überschreiten
        guest_token.expires_at = now() - timedelta(hours=1)
        guest_token.save()

        # Prüfen, ob das Token als abgelaufen erkannt wird
        self.assertTrue(guest_token.is_expired())

    def test_guest_login_deletes_expired_tokens(self):
        """Testet, ob abgelaufene Tokens automatisch gelöscht werden"""
        response = self.client.post(self.login_url, self.guest_customer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = CustomUser.objects.get(username="andrey")

        # Ablaufzeit überschreiten
        GuestToken.objects.filter(user=user).update(expires_at=now() - timedelta(hours=1))

        # Nochmal einloggen -> abgelaufene Tokens sollten gelöscht werden
        response = self.client.post(self.login_url, self.guest_customer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Prüfen, ob nur 1 aktuelles Token existiert
        self.assertEqual(GuestToken.objects.filter(user=user).count(), 1)