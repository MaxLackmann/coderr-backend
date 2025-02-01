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
        """Sortiert nach bestimmten Kriterien."""
        allowed_fields = ["updated_at", "min_price"]
        if ordering in allowed_fields or ordering.lstrip("-") in allowed_fields:
            if "min_price" in ordering:
                ordering_field = ordering.replace("min_price", "calculated_min_price")
                return offers.annotate(calculated_min_price=Min("details__price")).order_by(ordering_field)
            return offers.order_by(ordering)
        raise ValidationError({"detail": ["Ungültiges Sortierfeld. Erlaubte Felder: updated_at, min_price"]})

    @staticmethod
    def paginate_offers(request, offers):
        paginator = CustomPageNumberPagination()
        return paginator.paginate_queryset(offers, request), paginator

    @staticmethod
    def save_offer(data, user=None):
        serializer = OfferSerializer(data=data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        return serializer.save(user=user), serializer

    @staticmethod
    def retrieve_offer(offer_id):
        try:
            return Offer.objects.get(id=offer_id)
        except Offer.DoesNotExist:
            raise NotFound({"detail": ["Das angeforderte Angebot existiert nicht."]})

    @staticmethod
    def patch_offer(offer_id, data, user):
        offer, _ = OfferService.retrieve_offer(offer_id)
        if offer.user != user:
            raise PermissionDenied({"detail": ["Du kannst nur deine eigenen Angebote ändern."]})
        serializer = OfferSerializer(offer, data=data, partial=True)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        serializer.save()
        return offer, serializer

    @staticmethod
    def delete_offer(offer_id, user):
        offer, _ = OfferService.retrieve_offer(offer_id)
        if offer.user != user:
            raise PermissionDenied({"detail": ["Du kannst nur deine eigenen Angebote löschen."]})
        offer.delete()

    @staticmethod
    def retrieve_detailoffer(detailoffer_id):
        try:
            return DetailOffer.objects.get(id=detailoffer_id)
        except DetailOffer.DoesNotExist:
            raise NotFound({"detail": ["Das angeforderte Detail existiert nicht."]})