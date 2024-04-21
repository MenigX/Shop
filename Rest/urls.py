from django.urls import path, include
from .views import *
from rest_framework import routers


urlpatterns = [
    path('product/home/', ProductViewSet.as_view({'get':'list'})),
    path('product/desc/<int:pk>', ProductViewSet.as_view({'get': 'retrieve'})),
    path('product/create/', ProductViewSet.as_view({'post': 'post'})),
    path('order/create/', OrderViewSet.as_view({'post':'post'})),
    path('order/list/', OrderViewSet.as_view({'post':'list'})),


    
]