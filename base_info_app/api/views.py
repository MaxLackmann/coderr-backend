from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from base_info_app.api.serializers import BaseInfoSerializer
from user_app.models import CustomUser
from offers_app.models import Offer
from reviews_app.models import Review
from django.db.models import Avg


class BaseInfoView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        review_count = Review.objects.count()
        average_rating = Review.objects.all().aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        business_profile_count = CustomUser.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        data = {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count,
        }

        serializer = BaseInfoSerializer(data=data)
        return Response(data, status=status.HTTP_200_OK)