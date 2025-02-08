from django.db import models

class BaseInfo(models.Model):
    review_count = models.IntegerField()
    average_rating = models.DecimalField(max_digits=5, decimal_places=1)
    business_profile_count = models.IntegerField()
    offer_count = models.IntegerField()

    def __str__(self):
        return f"{self.review_count} reviews, {self.average_rating} average rating, {self.business_profile_count} business profiles, {self.offer_count} offers"
