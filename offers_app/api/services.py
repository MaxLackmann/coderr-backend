from offers_app.models import Offer, DetailOffer
from offers_app.api.serializers import OfferSerializer, DetailOfferSerializer
from offers_app.api.filters import OfferFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from offers_app.api.pagination import CustomPageNumberPagination
from django.db.models import Min, Q

class OfferService:
    @staticmethod
    def get_filtered_offers(request):
        offers = Offer.objects.prefetch_related("details").annotate(calculated_min_price=Min("details__price"))
        return offers

    @staticmethod
    def search_offers(offers, search_term):
        return offers.filter(Q(title__icontains=search_term) | Q(description__icontains=search_term)) if search_term else offers

    @staticmethod
    def sort_offers(offers, ordering):
        allowed_fields = ["updated_at", "min_price"]
        if ordering in allowed_fields or ordering.lstrip("-") in allowed_fields:
            if "min_price" in ordering:
                ordering_field = ordering.replace("min_price", "calculated_min_price")
                return offers.annotate(calculated_min_price=Min("details__price")).order_by(ordering_field)
            return offers.order_by(ordering)
        return offers
    
    @staticmethod
    def check_offer_user(offer, user):
        if offer.user != user:
            raise PermissionDenied()
        return offer

    @staticmethod
    def retrieve_offer(offer_id):
        return Offer.objects.get(id=offer_id)

    @staticmethod
    def retrieve_detailoffer(detailoffer_id):
        return DetailOffer.objects.get(id=detailoffer_id)