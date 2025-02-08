from rest_framework.response import Response
from rest_framework import status
from user_app.api.permissions import IsAuthenticatedOrGuest
from user_app.api.authentication import CombinedTokenAuthentication
from orders_app.models import Order
from offers_app.models import DetailOffer
from orders_app.api.serializers import OrderSerializer
from orders_app.api.services import OrderService
from rest_framework.views import APIView
from rest_framework.exceptions import  PermissionDenied
from orders_app.api.permissions import IsCustomerUser, IsOwnerOrderOrOffer

class OrderView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest, IsCustomerUser]

    def get(self, request):
        orders = OrderService.get_orders_for_user(request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        offer_detail_id = request.data.get("offer_detail_id")

        if not offer_detail_id:
            return Response({"detail": ["offer_detail_id wird benötigt."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = OrderService.create_order(offer_detail_id, request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except DetailOffer.DoesNotExist:
            return Response({"detail": ["Das angeforderte Angebotsdetail existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": ["Nur Kunden dürfen Bestellungen erstellen."]}, status=status.HTTP_403_FORBIDDEN)

class OrderDetailView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest, IsOwnerOrderOrOffer]

    def get(self, request, order_id):
        try:
            order = OrderService.retrieve_order(order_id)
            self.check_object_permissions(request, order)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"detail": ["Die angeforderte Bestellung existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": ["Nur der Bestellende kann diese Bestellung anschauen."]}, status=status.HTTP_403_FORBIDDEN)
        
    def patch(self, request, order_id):
        try:
            order = OrderService.retrieve_order(order_id)
            self.check_object_permissions(request, order)

            if not request.data or "status" not in request.data or len(request.data) > 1:
                return Response({"detail": ["Nur das Status-Feld darf aktualisiert werden."]}, status=status.HTTP_400_BAD_REQUEST)

            serializer = OrderSerializer(order, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({"detail": ["Ungültige Daten. Bitte überprüfe deine Eingabe."]}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"detail": ["Die angeforderte Bestellung existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": ["Nur Admin und der Bestellende kann diese Bestellung bearbeiten."]}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, order_id):
        try:
            order = OrderService.retrieve_order(order_id)
            self.check_object_permissions(request, order)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist:
            return Response({"detail": ["Die angeforderte Bestellung existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": ["Nur Admin kann diese Bestellung loeschen."]}, status=status.HTTP_403_FORBIDDEN)
        
    def put(self, request, order_id):
        return Response({"detail": ["Eine vollständige Aktualisierung ist nicht erlaubt."]}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class OrderCountView(APIView):
    def get(self, request, business_user_id):
        order_count = OrderService.count_orders_for_business(business_user_id, "in_progress")
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)
    
class CompletedOrderCountView(APIView):
    def get(self, request, business_user_id):
        completed_order_count = OrderService.count_orders_for_business(business_user_id, "completed")
        return Response({"completed_order_count": completed_order_count}, status=status.HTTP_200_OK)