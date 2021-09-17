from django.urls import path
from .views import *

app_name = 'patient'


urlpatterns = [
    path('search/', search, name='search'),
    path('add/', add, name='add'),
    path('all/', patients, name='all'),
    path('<uuid>/', patient_details, name='details'),
]
