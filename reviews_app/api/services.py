from reviews_app.models import Review


class ReviewService:
    @staticmethod
    def get_filtered_reviews(request):
        """
        Filter reviews based on the given request query parameters.

        Query parameters can be:
            - business_user_id: the ID of the business user who received the review
            - reviewer_id: the ID of the user who wrote the review

        Returns a queryset of reviews filtered by the given parameters.

        :param request: The request object to get query parameters from
        :return: A filtered queryset of reviews
        """

        reviews = Review.objects.all()

        business_user_id = request.query_params.get('business_user_id')
        reviewer_id = request.query_params.get('reviewer_id')

        if business_user_id and business_user_id.isdigit():
            reviews = reviews.filter(business_user_id=int(business_user_id))
        
        if reviewer_id and reviewer_id.isdigit():
            reviews = reviews.filter(reviewer_id=int(reviewer_id))

        if not reviews.exists():
            return []

        return reviews
    
    @staticmethod
    def sort_reviews(reviews, ordering):
        """
        Sorts the given queryset of reviews according to the specified ordering string.
    
        Args:
            reviews (QuerySet[Review]): The queryset of reviews to sort.
            ordering (str): The field to order by. Must be one of the following:
                * "updated_at"
                * "-updated_at"
                * "rating"
                * "-rating"
    
        Returns:
            QuerySet[Review]: The sorted queryset of reviews.
    
        Raises:
            ValueError: If the given ordering field is not allowed.
        """

        allowed_fields = ["updated_at", "-updated_at", "rating", "-rating"]
        if ordering in allowed_fields:
            return reviews.order_by(ordering)
        return reviews

    
    @staticmethod
    def retrieve_review(review_id):
        """
        Retrieves a review by its ID.

        :param review_id: The ID of the review to retrieve.
        :type review_id: int
        :return: The retrieved review.
        :rtype: Review
        :raises: Review.DoesNotExist if no review with the given ID exists.
        """

        return Review.objects.get(id=review_id)