from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from user_app.models import GuestToken

@receiver(post_save, sender=GuestToken)
def delete_expired_guest_tokens(sender, instance, **kwargs):
    """Löscht alle abgelaufenen Guest-Tokens, wenn ein neuer Token erstellt wird"""
    GuestToken.objects.filter(expires_at__lt=now()).delete()