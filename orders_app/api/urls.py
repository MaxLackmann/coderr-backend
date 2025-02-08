from django.urls import path
from .views import OrderView, OrderDetailView, OrderCountView, CompletedOrderCountView


urlpatterns = [
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='orders-detail'),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'), 
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-order-count'), 
]