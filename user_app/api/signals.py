from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from rest_framework.authtoken.models import Token
from datetime import timedelta
from user_app.models import CustomUser, GuestToken

@receiver(post_save, sender=Token)
def delete_expired_tokens(sender, instance, **kwargs):
    """
    Deletes expired Tokens after a new Token is saved.

    This receiver is set up to listen for the post_save signal from the Token model.
    It deletes all Tokens that are older than 24 hours.

    :param sender: The model class that sent the signal.
    :param instance: The actual instance of the model that sent the signal.
    :param kwargs: Extra keyword arguments passed in from the signal.
    :return: None
    """
    
    expiration_time = now() - timedelta(hours=24)
    deleted_count, _ = Token.objects.filter(created__lt=expiration_time).delete()
    if deleted_count > 0:
        print(f"Deleted {deleted_count} expired Tokens")

@receiver(post_save, sender=GuestToken)
def delete_expired_guest_tokens(sender, instance, **kwargs):
    """
    Deletes expired GuestTokens after a new GuestToken is saved.

    This receiver listens for the post_save signal from the GuestToken model.
    It deletes all GuestTokens that are older than 2 hours.

    :param sender: The model class that sent the signal.
    :param instance: The actual instance of the model that sent the signal.
    :param kwargs: Extra keyword arguments passed in from the signal.
    :return: None
    """

    expiration_time = now() - timedelta(hours=2)
    deleted_count, _ = GuestToken.objects.filter(created__lt=expiration_time).delete()
    if deleted_count > 0:
        print(f"Deleted {deleted_count} expired GuestTokens")

@receiver(post_save, sender=CustomUser)
def delete_inactive_tokens(sender, instance, **kwargs):
    """
    Deletes Tokens and GuestTokens for inactive CustomUsers after a new CustomUser is saved.

    This receiver listens for the post_save signal from the CustomUser model.
    It deletes all Tokens and GuestTokens associated with users who have been inactive
    for more than 1 hour.

    :param sender: The model class that sent the signal.
    :param instance: The actual instance of the model that sent the signal.
    :param kwargs: Extra keyword arguments passed in from the signal.
    :return: None
    """

    inactive_users = CustomUser.objects.filter(last_activity__lt=now() - timedelta(hours=1))

    if inactive_users.exists():
        deleted_count, _ = Token.objects.filter(user__in=inactive_users).delete()
        print(f"Deleted {deleted_count} expired Tokens for inactive users")

        deleted_guest_count, _ = GuestToken.objects.filter(user__in=inactive_users).delete()
        print(f"Deleted {deleted_guest_count} expired GuestTokens for inactive users")

