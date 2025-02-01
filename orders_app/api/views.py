from rest_framework.response import Response
from rest_framework import status
from user_app.api.permissions import IsAuthenticatedOrGuest
from user_app.api.authentication import CombinedTokenAuthentication
from orders_app.models import Order
from orders_app.api.serializers import OrderSerializer
from orders_app.api.services import OrderService
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

class OrderView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def post(self, request):
        try:
            detail_offer = OrderService.get_detail_offer(request.data.get('offer_detail_id'))
            order_data = OrderService.generate_order_data(request.user.id, detail_offer)

            serializer = OrderSerializer(data=order_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response(e.detail, status=status.HTTP_403_FORBIDDEN)


class OrderDetailView(APIView):
    pass