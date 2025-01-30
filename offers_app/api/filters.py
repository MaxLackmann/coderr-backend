import django_filters
from offers_app.models import Offer

class OfferFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="calculated_min_price", lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(field_name="details__delivery_time_in_days", lookup_expr='lte')
    creator_id = django_filters.NumberFilter(field_name="user_id", lookup_expr='exact')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']
