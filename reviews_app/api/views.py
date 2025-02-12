from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Review
from user_app.api.permissions import IsAuthenticatedOrGuest
from user_app.api.authentication import CombinedTokenAuthentication
from orders_app.api.permissions import IsCustomerUser
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from reviews_app.api.services import ReviewService
from reviews_app.api.permissions import CanModifyReview, CanCreateReview


class ReviewView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest, IsCustomerUser, CanCreateReview]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['rating', 'updated_at']

    def get(self, request):

        reviews = ReviewService.get_filtered_reviews(request)
        if reviews == []:
            return Response({'detail': ["Keine Bewertungen vorhanden"]}, status=status.HTTP_200_OK)
        
        reviews = ReviewService.sort_reviews(reviews, request.query_params.get('ordering', 'updated_at'))

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReviewDetailView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest, IsCustomerUser, CanModifyReview]

    def get(self, request, review_id):
        try:
            review = ReviewService.retrieve_review(review_id)
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({"detail": ["Die angeforderte Bewertung existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, review_id):
        try:
            review = ReviewService.retrieve_review(review_id)
            self.check_object_permissions(request, review)

            serializer = ReviewSerializer(review, data=request.data,context={'request': request}, partial=True)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({"detail": ["Die angeforderte Bewertung existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": ["Nicht Autorisiert zu bearbeiten."]}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, review_id):
        try:
            review = ReviewService.retrieve_review(review_id)
            self.check_object_permissions(request, review)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({"detail": ["Die angeforderte Bewertung existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": ["Nicht Autorisiert zu loeschen."]}, status=status.HTTP_403_FORBIDDEN)