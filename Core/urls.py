from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/', include("API.urls"))
]