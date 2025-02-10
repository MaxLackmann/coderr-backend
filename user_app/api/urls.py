from django.urls import path
from .views import RegistrationView, LoginView, ProfileView, BusinessProfilesView, CustomerProfilesView


urlpatterns = [
    path('registration/', RegistrationView.as_view() , name='registration'),
    path('login/', LoginView.as_view() , name='login'),
    path('profile/<int:pk>/', ProfileView.as_view() , name='profile'),
    path('profiles/business/', BusinessProfilesView.as_view() , name='business_profile'),
    path('profiles/customer/', CustomerProfilesView.as_view() , name='customer_profile'),
]