from django.test import TestCase
from django.utils.timezone import now, timedelta
from rest_framework.authtoken.models import Token
from user_app.models import CustomUser, GuestToken
from user_app.api.signals import delete_inactive_tokens, delete_expired_tokens, delete_expired_guest_tokens

class InactiveTokenDeletionTest(TestCase):

    def setUp(self):
        """Setup: Erstellt einen User für Tests"""
        self.user = CustomUser.objects.create_user(
            username="inactive_user",
            email="inactive@test.com",
            password="password123",
            type="customer"
        )

    def test_delete_token(self):
        token = Token.objects.create(user=self.user)
        Token.objects.filter(user=self.user).update(created=now() - timedelta(hours=24, minutes=1))

        self.assertTrue(Token.objects.filter(user=self.user).exists())

        delete_expired_tokens(sender=Token, instance=token)

        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_to_early_for_delete_token(self):
        token = Token.objects.create(user=self.user)
        Token.objects.filter(user=self.user).update(created=now() - timedelta(hours=23, minutes=59))
        
        self.assertTrue(Token.objects.filter(user=self.user).exists())

        delete_expired_tokens(sender=Token, instance=token)

        self.assertTrue(Token.objects.filter(user=self.user).exists())

    def test_delete_guest_token(self):
        guesttoken = GuestToken.objects.create(user=self.user)
        GuestToken.objects.filter(user=self.user).update(created=now() - timedelta(hours=2, minutes=1))

        self.assertTrue(GuestToken.objects.filter(user=self.user).exists())

        delete_expired_guest_tokens(sender=GuestToken, instance=guesttoken)

        self.assertFalse(GuestToken.objects.filter(user=self.user).exists())

    def test_to_early_for_delete_guest_token(self):
        guesttoken = GuestToken.objects.create(user=self.user)
        GuestToken.objects.filter(user=self.user).update(created=now() - timedelta(hours=1, minutes=59))
        
        self.assertTrue(GuestToken.objects.filter(user=self.user).exists())

        delete_expired_guest_tokens(sender=GuestToken, instance=guesttoken)

        self.assertTrue(GuestToken.objects.filter(user=self.user).exists())

    def test_inactive_token_deletion(self):
        self.user.last_activity = now() - timedelta(hours=1, minutes=1)
        self.user.save()

        token = Token.objects.create(user=self.user)
        self.assertTrue(Token.objects.filter(user=self.user).exists())

        delete_inactive_tokens(sender=CustomUser, instance=self.user)

        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_inactive_to_early_for_token_deletion(self):
        self.user.last_activity = now() - timedelta(minutes=59)
        self.user.save()

        token = Token.objects.create(user=self.user)
        self.assertTrue(Token.objects.filter(user=self.user).exists())

        delete_inactive_tokens(sender=CustomUser, instance=self.user)

        self.assertTrue(Token.objects.filter(user=self.user).exists())