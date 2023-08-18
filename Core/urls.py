from django.urls import path, include
from .views import *

urlpatterns = [
    path('', main),
    path('api/', include("API.urls"))
]