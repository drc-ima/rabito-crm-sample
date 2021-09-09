from django.urls import path
from .views import *

app_name = 'feedback'

urlpatterns = [
    path('setup/', setup, name="setup"),
    path('add-setup/', add_setup, name="add-setup"),
    path('setup-details/<uuid>/', setup_details, name="setup-details"),
]
