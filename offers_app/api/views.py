from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OfferSerializer
from rest_framework.authtoken.models import Token
from user_app.api.authentication import CombinedTokenAuthentication
from user_app.api.permissions import IsAuthenticatedOrGuest
from offers_app.models import Offer

class OffersView(APIView):
    permission_classes = [IsAuthenticatedOrGuest]
    

    def get(self, request):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OfferSerializer(data=request.data)

        if serializer.is_valid():
                offer = serializer.save(user=request.user) 
                return Response(OfferSerializer(offer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)