from django.urls import path
from .views import *

app_name = 'patient'


urlpatterns = [
    path('search/', search, name='search'),
    path('add/', add, name='add'),
]
