from django.urls import path
from .views import OffersView


urlpatterns = [
    path ('offers/', OffersView.as_view(), name='offers'),
    # path ('offerdetails/<int:offer_id>', views.OfferView.as_view(), name='offer'),
]