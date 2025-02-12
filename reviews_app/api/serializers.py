from rest_framework import serializers
from reviews_app.models import Review
from rest_framework.exceptions import ValidationError

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'reviewer']
    def validate_rating(self, value):
        """
        Validate the 'rating' field to ensure the value is not less than -1.
    
        Args:
            value (int): The rating.
    
        Returns:
            int: The validated rating.
    
        Raises:
            ValidationError: If the value is less than -1.
        """
        
        if value < -1:
            raise ValidationError({"detail": ["Revisions müssen mindestens 0 oder höher sein."]})
        return value

    def create(self, validated_data):
        """
        Creates and saves an instance of the Review model.

        The request body must contain the fields that should be created.

        Returns a JSON representation of the created review if the request is valid.

        Raises a 400 Bad Request error if the request body is invalid.

        The reviewer field is automatically set to the user that made the request.
        """

        request = self.context.get('request')
        validated_data['reviewer'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Updates an existing instance of the Review model.
    
        Only allows updating the 'rating' and 'description' fields. 
        If the validated data is empty, the instance is returned without changes.
    
        Args:
            instance (Review): The instance of the Review model to be updated.
            validated_data (dict): A dictionary of validated data to update the instance with.
    
        Returns:
            Review: The updated instance of the Review model.
        """

        allowed_fields = {"rating", "description"}
        filtered_data = {}
        for key, value in validated_data.items():
            if key in allowed_fields:
                filtered_data[key] = value

        if not validated_data:
            return instance

        return super().update(instance, validated_data)