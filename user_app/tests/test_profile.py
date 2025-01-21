from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token
from user_app.models import CustomUser
from unittest import skip
from django.utils.timezone import now

class ProfileTestCase(APITestCase):
    def setUp(self):
        self.customer = CustomUser.objects.create_user(
            username='testcustomer',
            email='testcustomer@test.de',
            password='password123',
            type='customer',
            first_name="Test",
            last_name="Customer",
            location="Berlin",
            tel="123456789",
            description="This is a test customer",
            working_hours="9-17"
        )
        self.customer.created_at = now()
        self.customer.save()

        self.business = CustomUser.objects.create_user(
            username='testbusiness',
            email='testbusiness@test.de',
            password='password123',
            type='business',
            first_name="Business",
            last_name="Owner",
            location="Hamburg",
            tel="987654321",
            description="This is a test business",
            working_hours="10-18"
        )
        self.business.created_at = now()
        self.business.save()
        
        self.client = APIClient()
        self.token = Token.objects.create(user=self.customer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.profile_url = reverse('profile', kwargs={'user_id': self.customer.id})
        self.business_profile_url = reverse('business_profile')
        self.customer_profile_url = reverse('customer_profile')

    def test_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testcustomer')
        self.assertEqual(response.data['email'], 'testcustomer@test.de')
        self.assertEqual(response.data['type'], 'customer')
        self.assertEqual(response.data['first_name'], "Test")
        self.assertEqual(response.data['last_name'], "Customer")
        self.assertEqual(response.data['location'], "Berlin")
        self.assertEqual(response.data['tel'], "123456789")
        self.assertEqual(response.data['description'], "This is a test customer")
        self.assertEqual(response.data['working_hours'], "9-17")
        self.assertEqual(response.data['file'], None)
        self.assertEqual(response.data['id'], self.customer.id)
        self.assertEqual(response.data['created_at'], self.customer.created_at.isoformat().replace("+00:00", "Z"))
        print(response.data)

    def test_get_business_profile(self):

        response = self.client.get(self.business_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testbusiness')
        self.assertEqual(response.data[0]['email'], 'testbusiness@test.de')
        self.assertEqual(response.data[0]['type'], 'business')

    def test_get_customer_profile(self):

        response = self.client.get(self.customer_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testcustomer')
        self.assertEqual(response.data[0]['email'], 'testcustomer@test.de')
        self.assertEqual(response.data[0]['type'], 'customer')