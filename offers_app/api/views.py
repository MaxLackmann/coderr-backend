from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import OfferSerializer
from user_app.api.authentication import CombinedTokenAuthentication
from user_app.api.permissions import IsAuthenticatedOrGuest
from offers_app.api.services import OfferService
from offers_app.api.pagination import CustomPageNumberPagination
from offers_app.models import Offer
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

class OffersView(APIView):
    permission_classes = [IsAuthenticatedOrGuest]
    # authentication_classes = [CombinedTokenAuthentication]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['creator_id', 'min_price', 'max_delivery_time']
    ordering_fields = ['min_price', 'updated_at']
    search_fields = ['title', 'description']

    def get(self, request):
        offers = OfferService.get_filtered_offers(request)
        
        offers = OfferService.search_offers(offers, request.query_params.get('search'))
        offers = OfferService.sort_offers(offers, request.query_params.get('ordering', 'min_price'))

        paginated_offers, paginator = OfferService.paginate_offers(request, offers)
        serializer = OfferSerializer(paginated_offers, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return response

    def post(self, request):
        offer, serializer = OfferService.save_offer(request.data, request.user)
        if offer:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OfferDetailView(APIView):
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request, offer_id):
        try:
            offer, serializer = OfferService.retrieve_offer(offer_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND) 
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST) 

    def patch(self, request, offer_id):
        try:
            offer, serializer = OfferService.patch_offer(offer_id, request.data, request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND) 
        except PermissionDenied as e:
            return Response(e.detail, status=status.HTTP_403_FORBIDDEN) 
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)  

    def delete(self, request, offer_id):
        try:
            OfferService.delete_offer(offer_id, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)  
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND) 
        except PermissionDenied as e:
            return Response(e.detail, status=status.HTTP_403_FORBIDDEN)  

class DetailOfferView(APIView):
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request, detailoffer_id):
        try:
            offer, serializer = OfferService.retrieve_detailoffer(detailoffer_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)