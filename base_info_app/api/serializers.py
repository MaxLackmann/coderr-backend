from rest_framework import serializers

class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.IntegerField(default=0)
    average_rating = serializers.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    business_profile_count = serializers.IntegerField(default=0)
    offer_count = serializers.IntegerField(default=0)