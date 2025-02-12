from reviews_app.models import Review
from user_app.models import CustomUser
from rest_framework.exceptions import PermissionDenied


class ReviewService:
    @staticmethod
    def get_filtered_reviews(request):
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
        allowed_fields = ["updated_at", "-updated_at", "rating", "-rating"]
        if ordering in allowed_fields:
            return reviews.order_by(ordering)
        return reviews

    
    @staticmethod
    def retrieve_review(review_id):
        return Review.objects.get(id=review_id)