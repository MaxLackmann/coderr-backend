from rest_framework import serializers
from offers_app.models import Offer, DetailOffer
from rest_framework.exceptions import ValidationError
from django.db.models import Min

class DetailOfferSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    class Meta:
        model = DetailOffer
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def validate_revisions(self, value):
        """
        Validate the 'revisions' field to ensure the value is not less than -1
        and not equal to 0. Raises a ValidationError if the condition is not met.
    
        Args:
            value (int): The number of revisions.
    
        Returns:
            int: The validated number of revisions.
    
        Raises:
            ValidationError: If the value is less than -1 or equal to 0.
        """

        if value < -1 or value == 0:
            raise ValidationError({"detail": ["Revisions müssen mindestens -1 oder höher sein."]})
        return value

    def validate_delivery_time_in_days(self, value):
        """
        Validate the 'delivery_time_in_days' field to ensure the value is greater than 0.

        Args:
            value (int): The delivery time in days.

        Returns:
            int: The validated delivery time in days.

        Raises:
            ValidationError: If the value is less than or equal to 0.
        """

        if value <= 0:
            raise ValidationError({"detail": ["Lieferzeit muss größer als 0 sein."]})
        return value

    def validate_price(self, value):
        """
        Validate the 'price' field to ensure the value is greater than 0.
    
        Args:
            value (int): The price.
    
        Returns:
            int: The validated price.
    
        Raises:
            ValidationError: If the value is less than or equal to 0.
        """

        if value <= 0:
            raise ValidationError({"detail": ["Preis darf nicht 0€ oder kleiner sein"]})
        return value
    
    def validate_features(self, value):
        """
        Validate the 'features' field to ensure the value is not empty.
    
        Args:
            value (list): The list of features.
    
        Returns:
            list: The validated list of features.
    
        Raises:
            ValidationError: If the value is an empty list.
        """

        if len(value) == 0:
            raise ValidationError({"detail": ["mindestens 1 Feature erforderlich."]})
        return value
    
    def update(self, instance, validated_data):
        """
        Updates and saves an instance of the DetailOffer model.

        Args:
            instance (DetailOffer): The instance of the DetailOffer model to be updated.
            validated_data (dict): A dictionary of validated data to update the instance with.

        Returns:
            DetailOffer: The updated instance of the DetailOffer model.
        """

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = DetailOfferSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at' ,'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_min_price(self, obj):
        """
        Returns the minimum price of the offer's details.
        
        Args:
            obj (Offer): The offer instance.
        
        Returns:
            int: The minimum price of the offer's details.
        """

        return obj.details.aggregate(Min("price"))["price__min"]

    def get_min_delivery_time(self, obj):
        """
        Returns the minimum delivery time of the offer's details.
        
        Args:
            obj (Offer): The offer instance.
        
        Returns:
            int: The minimum delivery time of the offer's details.
        """

        return obj.details.aggregate(Min("delivery_time_in_days"))["delivery_time_in_days__min"]
    
    def get_user_details(self, obj):
        """
        Returns a dictionary containing the first name, last name and username of the user that created the offer.
        
        Args:
            obj (Offer): The offer instance.
        
        Returns:
            dict: A dictionary containing the first name, last name and username of the offer's user.
        """

        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username
        }

    def validate_details(self, value):
        """
        Validate the 'details' field to ensure it contains 3 details, each with a different type (basic, standard, premium).

        Args:
            value (list): The list of details.

        Returns:
            list: The validated list of details.

        Raises:
            ValidationError: If the value does not contain 3 details with different types.
        """

        if len(value) != 3:
            raise ValidationError({"detail": ["3 Details erforderlich"]})
        
        offer_types = {detail['offer_type'] for detail in value}
        required_type = {'basic', 'standard', 'premium'}

        if offer_types != required_type:
            raise serializers.ValidationError({"detail": ["1 Basic, 1 Standard und 1 Premium Details erforderlich"]})
        
        return value

    def create(self, validated_data):
        """
        Creates and saves an instance of the Offer model, and creates and saves 
        the related DetailOffer instances.

        Args:
            validated_data (dict): A dictionary of validated data to create the instance with.

        Returns:
            Offer: The created instance of the Offer model.
        """

        details_data = validated_data.pop('details', [])

        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            DetailOffer.objects.create(offer=offer, **detail_data)

        return offer
        
    def update_instance_with_details(instance, validated_data):
        """
        Updates an existing instance of the Offer model and its related DetailOffer instances.

        Args:
            instance (Offer): The existing Offer instance to update.
            validated_data (dict): A dictionary of validated data to update the instance with.

        Returns:
            Offer: The updated instance of the Offer model.
        """
        
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if not details_data:
            return instance

        existing_details = {detail.offer_type: detail for detail in instance.details.all()}

        for detail in details_data:
            detail_instance = existing_details.get(detail["offer_type"])
            if detail_instance:
                for attr, value in detail.items():
                    setattr(detail_instance, attr, value)
                detail_instance.save()

        return instance