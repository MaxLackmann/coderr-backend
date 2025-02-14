from offers_app.models import Offer, DetailOffer
from rest_framework.exceptions import PermissionDenied
from django.db.models import Min, Q

class OfferService:
    @staticmethod
    def get_filtered_offers(request):
        """
        Filter offers based on the given request query parameters.

        Query parameters can be: creator_id, min_price, max_delivery_time

        :param request: The request object to get query parameters from
        :return: A filtered queryset of offers
        """

        offers = Offer.objects.prefetch_related("details").annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days")
        )

        filters = Q()
        creator_id = request.query_params.get("creator_id")
        min_price = request.query_params.get("min_price")
        max_delivery_time = request.query_params.get("max_delivery_time")

        if creator_id:
            filters &= Q(user_id=creator_id)
        if min_price:
            filters &= Q(min_price__gte=min_price)
        if max_delivery_time:
            filters &= Q(min_delivery_time__lte=max_delivery_time)

        return offers.filter(filters)

    @staticmethod
    def search_offers(offers, search_term):
        """
        Searches the given queryset of offers according to the given search term.

        Args:
            offers (QuerySet[Offer]): The queryset of offers to search.
            search_term (str): The term to search for.

        Returns:
            QuerySet[Offer]: The filtered queryset of offers where the title or description contains the given search term.

        Note: The search is case insensitive.
        """

        if search_term:
            return offers.filter(Q(title__icontains=search_term) | Q(description__icontains=search_term))
        return offers

    @staticmethod
    def sort_offers(offers, ordering):
        """
        Sorts the given queryset of offers according to the given ordering string.

        Args:
            offers (QuerySet[Offer]): The queryset of offers to sort.
            ordering (str): The field to order by.

        Returns:
            QuerySet[Offer]: The sorted queryset of offers.

        Raises:
            ValueError: If the given ordering field is not one of the following:
                * "updated_at"
                * "-updated_at"
                * "min_price"
                * "-min_price"

        Note: When ordering by "min_price", the "calculated_min_price" annotation is used
        to calculate the minimum price for each offer. This annotation is then used to
        order the queryset.
        """

        allowed_fields = ["updated_at", "-updated_at", "min_price", "-min_price"]
    
        if ordering in allowed_fields:
            if "min_price" in ordering:
                ordering_field = ordering.replace("min_price", "calculated_min_price")
                return offers.annotate(calculated_min_price=Min("details__price")).order_by(ordering_field)
            return offers.order_by(ordering)
    
        return offers

    @staticmethod
    def retrieve_offer(offer_id):
        """
        Retrieve an Offer object by its ID, including the minimum price and delivery time
        of all its related DetailOffer objects.
        
        :param offer_id: The ID of the Offer object to retrieve.
        :return: The retrieved Offer object.
        :raises: Offer.DoesNotExist if no Offer with the given ID exists.
        """
        
        return Offer.objects.prefetch_related("details").annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days")
        ).get(id=offer_id)
    
    @staticmethod
    def retrieve_detailoffer(detailoffer_id):
        """
        Retrieve a DetailOffer object by its ID.
    
        Args:
            detailoffer_id (int): The ID of the DetailOffer to retrieve.
    
        Returns:
            DetailOffer: The DetailOffer instance corresponding to the given ID.
    
        Raises:
            DetailOffer.DoesNotExist: If no DetailOffer with the given ID is found.
        """

        return DetailOffer.objects.get(id=detailoffer_id)