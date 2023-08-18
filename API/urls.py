from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', AccountViewSet.as_view({'post': 'login'})),
    path('retrieve/', AccountViewSet.as_view({'post': 'retrieve'}))
]