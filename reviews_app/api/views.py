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
        """
        Retrieve a list of reviews filtered by query parameters.

        Query parameters can be:
            - reviewer: the ID of the reviewer
            - business_user: the ID of the business user being reviewed
            - ordering: the field to order the reviews by (rating or updated_at)

        Returns a paginated list of reviews.
        """

        reviews = ReviewService.get_filtered_reviews(request)

        if not reviews:
            return Response([], status=status.HTTP_200_OK)

        reviews = ReviewService.sort_reviews(reviews, request.query_params.get('ordering', 'updated_at'))

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        """
        Create a new review.

        The request body must contain the fields that should be created.

        Returns a JSON representation of the created review if the request is valid.

        Raises a 400 Bad Request error if the request body is invalid.

        The reviewer field is automatically set to the user that made the request.
        """

        serializer = ReviewSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReviewDetailView(APIView):
    authentication_classes = [CombinedTokenAuthentication]
    permission_classes = [IsAuthenticatedOrGuest, IsCustomerUser, CanModifyReview]

    def get(self, request, review_id):
        """
        Retrieves a review by its ID.

        :param review_id: The ID of the review to retrieve.
        :return: A JSON representation of the retrieved review if it exists.
        :raises: 404 Not Found if the review does not exist.
        """

        try:
            review = ReviewService.retrieve_review(review_id)
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({"detail": ["Die angeforderte Bewertung existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, review_id):
        """
        Updates an existing review by its ID.

        The request body must contain the fields that should be updated.

        Returns a JSON representation of the updated review if the request is valid.

        Raises a 400 Bad Request error if the request body is invalid.

        Raises a 403 Forbidden error if the user is not the owner of the review.

        Raises a 404 Not Found error if the review does not exist.
        """

        try:
            review = ReviewService.retrieve_review(review_id)
            self.check_object_permissions(request, review)

            serializer = ReviewSerializer(review, data=request.data,context={'request': request}, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({"detail": ["Die angeforderte Bewertung existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": ["Nicht Autorisiert zu bearbeiten."]}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, review_id):
        """
        Deletes a review by its ID.

        Raises a 404 Not Found error if the review does not exist.

        Raises a 403 Forbidden error if the user is not the owner of the review.

        Returns a 204 No Content response if the review is successfully deleted.
        """

        try:
            review = ReviewService.retrieve_review(review_id)
            self.check_object_permissions(request, review)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({"detail": ["Die angeforderte Bewertung existiert nicht."]}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": ["Nicht Autorisiert zu loeschen."]}, status=status.HTTP_403_FORBIDDEN)