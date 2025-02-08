from orders_app.models import Order
from offers_app.models import DetailOffer
from django.db.models import Q

class OrderService:

    @staticmethod
    def get_orders_for_user(user):
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).distinct()
    
    @staticmethod
    def create_order(offer_detail_id, customer_user):
        offer_detail = DetailOffer.objects.get(id=offer_detail_id)

        order = Order.objects.create(
            customer_user=customer_user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title, 
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress",
        )

        return order
    
    @staticmethod
    def retrieve_order(order_id):
        return Order.objects.get(id=order_id)

    @staticmethod
    def count_orders_for_business(business_user_id, status):
        return Order.objects.filter(business_user_id=business_user_id, status=status).count()