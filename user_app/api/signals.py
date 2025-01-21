from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from rest_framework.authtoken.models import Token
from datetime import timedelta
from user_app.models import CustomUser, GuestToken

@receiver(post_save, sender=Token)
def delete_expired_tokens(sender, instance, **kwargs):
    expiration_time = now() - timedelta(hours=24)
    deleted_count, _ = Token.objects.filter(created__lt=expiration_time).delete()
    if deleted_count > 0:
        print(f"Deleted {deleted_count} expired Tokens")

@receiver(post_save, sender=GuestToken)
def delete_expired_guest_tokens(sender, instance, **kwargs):
    expiration_time = now() - timedelta(hours=2)
    deleted_count, _ = GuestToken.objects.filter(created__lt=expiration_time).delete()
    if deleted_count > 0:
        print(f"Deleted {deleted_count} expired GuestTokens")

@receiver(post_save, sender=CustomUser)
def delete_inactive_tokens(sender, instance, **kwargs):
    inactive_users = CustomUser.objects.filter(last_activity__lt=now() - timedelta(hours=1))

    if inactive_users.exists():
        deleted_count, _ = Token.objects.filter(user__in=inactive_users).delete()
        print(f"Deleted {deleted_count} expired Tokens for inactive users")

        deleted_guest_count, _ = GuestToken.objects.filter(user__in=inactive_users).delete()
        print(f"Deleted {deleted_guest_count} expired GuestTokens for inactive users")

