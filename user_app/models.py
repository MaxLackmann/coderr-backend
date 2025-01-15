from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]

    email = models.EmailField(unique=True)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    # file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
    # location = models.CharField(max_length=255, null=True, blank=True)
    # tel = models.CharField(max_length=20, null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    # working_hours = models.CharField(max_length=50, null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.type})"