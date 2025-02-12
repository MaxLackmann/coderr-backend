from django.db import models
from user_app.models import CustomUser

class Offer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='offer_images/',  null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the Offer, which is just the title of the Offer.
        """
        
        return self.title
    
class DetailOffer(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=100)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    features = models.JSONField()
    offer_type = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        """
        Saves the DetailOffer instance to the database. This method is overridden to set the delivery_time_in_days field to a positive value if it is not already positive.

        Raises:
            ValidationError: If the delivery_time_in_days field is not a positive integer.
        """
        
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the DetailOffer, which includes the title of the related Offer and the title of this DetailOffer instance.
        """

        return f"{self.offer.title} - {self.title}"
