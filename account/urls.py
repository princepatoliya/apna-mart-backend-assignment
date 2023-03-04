from django.urls import path, include
from account.views import UserRegistrationView, UserLoginView, UserProfileView

urlpatterns = [
  path('auth/register/', UserRegistrationView.as_view(), name='register'),
  path('auth/login/', UserLoginView.as_view(), name='login'),
  path('profile/', UserProfileView.as_view(), name='profile'),
]
