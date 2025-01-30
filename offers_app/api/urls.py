from django.urls import path
from .views import OffersView, OfferDetailView, DetailOfferView


urlpatterns = [
    path ('offers/', OffersView.as_view(), name='offers'),
    path ('offers/<int:offer_id>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:detailoffer_id>/', DetailOfferView.as_view(), name='detail-offer'),
]