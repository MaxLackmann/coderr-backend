from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from user_app.models import GuestToken

@receiver(post_save, sender=GuestToken)
def delete_expired_guest_tokens(sender, instance, **kwargs):
    """Löscht ALLE abgelaufenen GuestTokens automatisch"""
    deleted_count, _ = GuestToken.objects.filter(expires_at__lt=now()).delete()
    if deleted_count > 0:
        print(f" Deleted {deleted_count} expired GuestTokens")