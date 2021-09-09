from django.urls import path

from . views import *

app_name = 'commissiion'

urlpatterns = [
    path('setups/', commission_setups, name='setups')
]
