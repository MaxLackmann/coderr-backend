from orders_app.models import Order
from offers_app.models import DetailOffer
from django.db.models import Q

class OrderService:

    @staticmethod
    def get_orders_for_user(user):
        """
        Returns a QuerySet of orders associated with the given user.
    
        :param user: The user to get orders for.
        :type user: user_app.models.CustomUser
        :return: A QuerySet of orders associated with the given user.
        :rtype: django.db.models.QuerySet
        """
        
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).distinct()
    
    @staticmethod
    def create_order(offer_detail_id, customer_user):
        """
        Creates a new order using the given offer detail and customer user.

        :param offer_detail_id: The ID of the offer detail to use for the order.
        :type offer_detail_id: int
        :param customer_user: The user that is placing the order.
        :type customer_user: user_app.models.CustomUser
        :return: The newly created order.
        :rtype: orders_app.models.Order
        """

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
        """
        Retrieves an order by its ID.

        :param order_id: The ID of the order to retrieve.
        :type order_id: int
        :return: The retrieved order.
        :rtype: orders_app.models.Order
        :raises: Order.DoesNotExist if no order with the given ID exists.
        """
        return Order.objects.get(id=order_id)

    @staticmethod
    def count_orders_for_business(business_user_id, status):
        """
        Counts the number of orders for a given business user with a given status.

        :param business_user_id: The ID of the business user to count orders for.
        :type business_user_id: int
        :param status: The status of the orders to count.
        :type status: str
        :return: The number of orders for the given business user with the given status.
        :rtype: int
        """
        return Order.objects.filter(business_user_id=business_user_id, status=status).count()