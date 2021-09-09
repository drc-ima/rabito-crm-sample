from django.urls import path
from .views import *
app_name = 'schedule'


urlpatterns = [
    path('weekly/', weekly, name='weekly'),
    path('daily/', daily, name='daily'),
    path('<uuid>/', planner_details, name='details'),
]
