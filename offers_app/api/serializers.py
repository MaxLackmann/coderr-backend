from rest_framework import serializers
from offers_app.models import Offer, DetailOffer
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

class DetailOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailOffer
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = DetailOfferSerializer(many=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description','details', 'created_at', 'updated_at']

    def validate_details(self, value):
        if len(value) < 3:
            raise ValidationError({"details": ["Mindestens 3 Details erforderlich"]})
        
        offer_types = {detail['offer_type'] for detail in value}
        required_type = {'basic', 'standard', 'premium'}

        if offer_types != required_type:
            raise serializers.ValidationError({"details": ["Mindestens 1 Basic, 1 Standard und 1 Premium Details erforderlich"]})
        
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])

        try:
            offer = Offer.objects.create(**validated_data)
            for detail_data in details_data:
                DetailOffer.objects.create(offer=offer, **detail_data)
            return offer
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)


