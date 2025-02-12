from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user_app.models import CustomUser
from offers_app.models import Offer
from reviews_app.models import Review


class BaseInfoView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Returns a JSON response containing statistics about the database.

        Statistics include:

        - review_count: Total number of reviews.
        - average_rating: Average rating of all reviews, rounded to one decimal place.
        - business_profile_count: Total number of business profiles.
        - offer_count: Total number of offers.

        :param request: The request object.
        :return: A JSON response containing the statistics with an HTTP 200 OK status.
        """

        return Response(self._get_statistics(), status=status.HTTP_200_OK)

    def _get_statistics(self):
        """
        Collects statistics for reviews, business profiles, and offers.
    
        Returns a dictionary containing:
        - review_count: Total number of reviews.
        - average_rating: Average rating of all reviews, rounded to one decimal place.
        - business_profile_count: Total number of business profiles.
        - offer_count: Total number of offers.
        """

        avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0.0
        return {
            'review_count': Review.objects.count(),
            'average_rating': round(avg_rating, 1),
            'business_profile_count': CustomUser.objects.filter(type='business').count(),
            'offer_count': Offer.objects.count(),
        }
