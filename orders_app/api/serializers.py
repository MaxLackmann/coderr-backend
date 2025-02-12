from rest_framework import serializers
from orders_app.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'customer_user', 'business_user', 'created_at']   

    def update(self, instance, validated_data):
        """
        Updates and saves an instance of the Order model.

        The request body must contain the fields that should be updated.

        Returns a JSON representation of the updated order if the request is valid.

        Raises a 400 Bad Request error if the request body is invalid.

        Raises a 403 Forbidden error if the user is not the owner of the order.
        """

        if 'status' in validated_data:
            instance.status = validated_data.pop('status')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance