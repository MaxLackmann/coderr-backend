from django.urls import path
from .views import OrderView, OrderDetailView


urlpatterns = [
    path ('orders/', OrderView.as_view(), name='offers'),
    path ('orders/<int:offer_id>/', OrderDetailView.as_view(), name='offer-detail'),
]