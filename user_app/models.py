from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]

    email = models.EmailField(unique=True)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=50, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=now)

    def update_activity(self):
        self.last_activity = now()
        self.save(update_fields=['last_activity'])

    def is_inactive(self):
        return now() > self.last_activity + timedelta(hours=1)

    def __str__(self):
        return f"{self.username} ({self.type})"
    
class GuestToken(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="guest_tokens")
    key = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now() > self.created + timedelta(hours=2)
