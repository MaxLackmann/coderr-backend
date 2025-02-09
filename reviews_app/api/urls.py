from django.urls import path
from .views import ReviewView, ReviewDetailView


urlpatterns = [
    path('reviews/', ReviewView.as_view(), name='reviews-list'),
    path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
]