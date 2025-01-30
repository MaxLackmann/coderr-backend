from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from offers_app.models import Offer, DetailOffer


class OfferDetailTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='test123',
            email='testuser@test.de'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.offer = Offer.objects.create(
                    user=self.user,
                    title="Grafikdesign Paket",
                    description="Design für Unternehmen..."
                )
        
        self.detail_url = reverse('offer-detail', kwargs={'offer_id': self.offer.id})

        details = [
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

        for detail in details:
            DetailOffer.objects.create(offer=self.offer, **detail)

    def test_get_offer_by_id(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.offer.id)
        

    def test_get_offer_by_id_invalid(self):
        non_existent_url = reverse('offer-detail', kwargs={'offer_id': 999})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('detail'), ["Das angeforderte Angebot existiert nicht."])