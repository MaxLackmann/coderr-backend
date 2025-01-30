from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from offers_app.models import Offer, DetailOffer

class GetOfferTest(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser1',
            password='test123',
            email='testuser1@test.de'
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            password='test123',
            email='testuser2@test.de'
        )

        self.get_url = reverse('offers')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

        self.offer1 = Offer.objects.create(
            user=self.user1,
            title="Website Design",
            description="Professionelles Website-Design..."
        )
        self.offer2 = Offer.objects.create(
            user=self.user2,
            title="Grafikdesign Paket",
            description="Design für Unternehmen..."
        )

        details1 = [
            {
                "title": "Basic",
                "revisions": 2,
                "delivery_time_in_days": 5,
                "price": 100.00,
                "features": ["Logo"],
                "offer_type": "basic"
            },
            {
                "title": "Standard",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 200.00,
                "features": ["Logo", "Visitenkarte"],
                "offer_type": "standard"
            },
            {
                "title": "Premium",
                "revisions": 10,
                "delivery_time_in_days": 10,
                "price": 500.00,
                "features": ["Logo", "Visitenkarte", "Flyer"],
                "offer_type": "premium"
            }
        ]

        details2 = [
            {
                "title": "Basic",
                "revisions": 2,
                "delivery_time_in_days": 4,
                "price": 90.00,
                "features": ["Logo"],
                "offer_type": "basic"
            },
            {
                "title": "Standard",
                "revisions": 5,
                "delivery_time_in_days": 6,
                "price": 180.00,
                "features": ["Logo", "Visitenkarte"],
                "offer_type": "standard"
            },
            {
                "title": "Premium",
                "revisions": 10,
                "delivery_time_in_days": 9,
                "price": 400.00,
                "features": ["Logo", "Visitenkarte", "Flyer"],
                "offer_type": "premium"
            }
        ]

        for detail in details1:
            DetailOffer.objects.create(offer=self.offer1, **detail)

        for detail in details2:
            DetailOffer.objects.create(offer=self.offer2, **detail)

    def test_get_all_offers(self):
        response = self.client.get(self.get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_pagination(self):
        response = self.client.get(self.get_url, {"page": 1, "page_size": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_by_creator_id(self):
        response = self.client.get(self.get_url, {"creator_id": self.user1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_min_price(self):
        response = self.client.get(self.get_url, {"min_price": 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(
            min(detail["price"] for detail in offer["details"]) >= 100
            for offer in response.data["results"]
        ))

    def test_filter_by_max_delivery_time(self):
        response = self.client.get(self.get_url, {"max_delivery_time": 7})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(offer["details"][0]["delivery_time_in_days"] <= 7 for offer in response.data["results"]))

    def test_search_offers(self):
        response = self.client.get(self.get_url, {"search": "Website"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_sort_by_min_price(self):
        response = self.client.get(self.get_url, {"ordering": "min_price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [offer["details"][0]["price"] for offer in response.data["results"]]
        self.assertEqual(prices, sorted(prices))

    def test_sort_by_min_price_desc(self):
        response = self.client.get(self.get_url, {"ordering": "-min_price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [offer["details"][0]["price"] for offer in response.data["results"]]
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_sort_by_updated_at(self):
        response = self.client.get(self.get_url, {"ordering": "updated_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_at = [offer["updated_at"] for offer in response.data["results"]]
        self.assertEqual(updated_at, sorted(updated_at))

    def test_sort_by_updated_at_desc(self):
        response = self.client.get(self.get_url, {"ordering": "-updated_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_at = [offer["updated_at"] for offer in response.data["results"]]
        self.assertEqual(updated_at, sorted(updated_at, reverse=True))

    def test_sort_with_invalid_field(self):
        response = self.client.get(self.get_url + "?ordering=invalid_field")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ordering", response.data)