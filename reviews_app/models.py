from django.db import models
from user_app.models import CustomUser

class Review(models.Model):
    business_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='written_reviews')
    rating = models.IntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Saves the Review instance to the database. This method is overridden to
        add the current date and time to the 'updated_at' field.
        """
        
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the Review, which includes the reviewer's username and the business user's username.
        """

        return f"Review by {self.reviewer} for {self.business_user}"