from django.urls import path
from .views import ReviewView, ReviewDetailView


urlpatterns = [
    path('reviews/', ReviewView.as_view(), name='base-info'),
    path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='base-info'),
]