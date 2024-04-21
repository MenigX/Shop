from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('authorize/', AuthorizationView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('tokens/', ListTokenView.as_view()),
]