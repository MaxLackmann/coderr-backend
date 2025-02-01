from orders_app.models import Order
from offers_app.models import DetailOffer
from orders_app.api.serializers import OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied


class OrderService:
    @staticmethod
    def get_detail_offer(offer_detail_id):
        if not offer_detail_id:
            raise ValidationError({"detail": "offer_detail_id ist erforderlich"})
        try:
            return DetailOffer.objects.get(id=offer_detail_id)
        except DetailOffer.DoesNotExist:
            raise NotFound({"detail": "DetailOffer nicht gefunden."})

    @staticmethod
    def generate_order_data(user_id, detail_offer):
        return {
            "custom_user": user_id,
            "business_user": detail_offer.user.id,
            "detail_offer": detail_offer.id,
            "title": detail_offer.title,
            "revisions": detail_offer.revisions,
            "delivery_time_in_days": detail_offer.delivery_time_in_days,
            "price": detail_offer.price,
            "features": detail_offer.features,
            "offer_type": detail_offer.offer_type,
        }