from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import OfferSerializer, DetailOfferSerializer
from user_app.api.authentication import CombinedTokenAuthentication
from user_app.api.permissions import IsAuthenticatedOrGuest
from offers_app.api.services import OfferService
from offers_app.api.pagination import CustomPageNumberPagination
from offers_app.models import Offer, DetailOffer
from rest_framework.exceptions import PermissionDenied
from offers_app.api.permissions import IsBusinessUser

class OffersView(APIView):
    permission_classes = [IsAuthenticatedOrGuest, IsBusinessUser]
    authentication_classes = [CombinedTokenAuthentication]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['creator_id', 'min_price', 'max_delivery_time']
    ordering_fields = ['min_price', 'updated_at']
    search_fields = ['title', 'description']

    def get(self, request):
        offers = OfferService.get_filtered_offers(request)
        offers = OfferService.search_offers(offers, request.query_params.get('search'))
        offers = OfferService.sort_offers(offers, request.query_params.get('ordering', 'min_price'))

        paginator = CustomPageNumberPagination()
        paginated_offers = paginator.paginate_queryset(offers, request)
        serializer = OfferSerializer(paginated_offers, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        try:
            serializer = OfferSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"detail": ["Ungültige Daten. Bitte überprüfe deine Eingabe."]}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except PermissionDenied:
            return Response({"detail": ["Nur Geschäftsnutzer dürfen Angebote erstellen."]}, status=status.HTTP_403_FORBIDDEN)

class OfferDetailView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request, offer_id):
        try:
            offer = OfferService.retrieve_offer(offer_id)
            serializer = OfferSerializer(offer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Offer.DoesNotExist:
            return Response({"detail": ["Das angeforderte Angebot existiert nicht."]}, status=status.HTTP_404_NOT_FOUND) 

    def patch(self, request, offer_id):
        try:
            offer = OfferService.retrieve_offer(offer_id)
            OfferService.check_offer_user(offer, request.user)

            serializer = OfferSerializer(offer, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({"detail": ["Ungültige Daten. Bitte überprüfe deine Eingabe."]}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Offer.DoesNotExist:
            return Response({"detail": ["Das angeforderte Angebot existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": ["Nicht Autorisiert zu bearbeiten."]}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, offer_id):
        try:
            offer = OfferService.retrieve_offer(offer_id)
            OfferService.check_offer_user(offer, request.user)
            offer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Offer.DoesNotExist:
            return Response({"detail": ["Das angeforderte Angebot existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": ["Nicht Autorisiert zu loeschen."]}, status=status.HTTP_403_FORBIDDEN)

class DetailOfferView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest]

    def get(self, request, detailoffer_id):
        try:
            detailoffer = OfferService.retrieve_detailoffer(detailoffer_id)
            serializer = DetailOfferSerializer(detailoffer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DetailOffer.DoesNotExist:
            return Response({"detail": ["Das angeforderte Detail existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)