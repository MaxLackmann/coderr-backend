from rest_framework import serializers
from offers_app.models import Offer, DetailOffer
from rest_framework.exceptions import ValidationError

class DetailOfferSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    class Meta:
        model = DetailOffer
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def validate_revisions(self, value):
        if value < -1:
            raise ValidationError({"detail": ["Revisions müssen mindestens -1 oder höher sein."]})
        return value

    def validate_delivery_time(self, value):
        if value < 0:
            raise ValidationError({"detail": ["Lieferzeit muss größer als 0 sein."]})
        return value

    def validate_price(self, value):
        if value < 0:
            raise ValidationError({"detail": ["Preis darf nicht negativ sein."]})
        return value
    
    def validate_features(self, value):
        if len(value) == 0:
            raise ValidationError({"detail": ["mindestens 1 Feature erforderlich."]})
        return value
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = DetailOfferSerializer(many=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at' ,'details']

    def validate_image(self, value):
        if value is not None:
            raise ValidationError({"detail": ["'image' darf nicht vorhanden sein."]})
        return value

    def validate_details(self, value):
        if len(value) != 3:
            raise ValidationError({"detail": ["3 Details erforderlich"]})
        
        offer_types = {detail['offer_type'] for detail in value}
        required_type = {'basic', 'standard', 'premium'}

        if offer_types != required_type:
            raise serializers.ValidationError({"detail": ["1 Basic, 1 Standard und 1 Premium Details erforderlich"]})
        
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])

        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            DetailOffer.objects.create(offer=offer, **detail_data)

        return offer
        
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            existing_details = {}
            for detail_offer in instance.details.all():
                existing_details[detail_offer.offer_type] = detail_offer

            for detail_data in details_data:
                detail_instance = existing_details.get(detail_data["offer_type"])
                if detail_instance:
                    for attr, value in detail_data.items():
                        setattr(detail_instance, attr, value)
                    detail_instance.save()

        return instance

