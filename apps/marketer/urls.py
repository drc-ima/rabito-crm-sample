from django.urls import path
from .views import *

app_name = 'marketer'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard')
]
