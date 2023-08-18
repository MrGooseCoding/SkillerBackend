from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', AccountViewSet.as_view({'post': 'login'})),
    path('retrieve/', AccountViewSet.as_view({'post': 'retrieve'})),
    path('search/', AccountViewSet.as_view({'post': 'search'})),
    path('create/', AccountViewSet.as_view({'post': 'create'}))

]