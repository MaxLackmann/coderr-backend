from rest_framework import serializers
from reviews_app.models import Review
from rest_framework.exceptions import ValidationError

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'reviewer']
    def validate_rating(self, value):
        if value < -1:
            raise ValidationError({"detail": ["Revisions müssen mindestens 0 oder höher sein."]})
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['reviewer'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        allowed_fields = {"rating", "description"}
        filtered_data = {}
        for key, value in validated_data.items():
            if key in allowed_fields:
                filtered_data[key] = value

        if not validated_data:
            return instance

        return super().update(instance, validated_data)