from rest_framework import serializers
from orders_app.models import Order

class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICE, required=False)
    class Meta:
        model = Order
        fields = ['id', 'custom_user', 'business_user', 
                    'title', 'revisions', 'delivery_time_in_days', 'price',
                    'features', 'offer_type', 'status', 'created_at', 'updated_at']