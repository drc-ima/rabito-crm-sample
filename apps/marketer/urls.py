from django.urls import path
from .views import *

app_name = 'marketer'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('engagements/', engagements, name='engagements'),
    path('partners/', partners, name='partners'),
    path('add-partner/', add_partner, name='add-partner'),
]
