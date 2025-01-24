from django.db import models
from user_app.models import CustomUser
from django.core.exceptions import ValidationError

class Offer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='offer_images/',  null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class DetailOffer(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=100)
    
    def clean(self):
        """ Validierung für revisions, delivery_time_in_days und price """
        errors = {}

        if self.revisions < -1:
            errors["revisions"] = "Revisions müssen mindestens -1 oder höher sein."
        if self.delivery_time_in_days <= 0:
            errors["delivery_time_in_days"] = "Delivery Time muss größer als 0 sein."
        if self.price < 0:
            errors["price"] = "Price darf nicht negativ sein."

        if errors:
            raise ValidationError(errors)
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.offer.title} - {self.title}"
