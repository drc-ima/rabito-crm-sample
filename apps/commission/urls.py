from django.urls import path

from . views import *

app_name = 'commissiion'

urlpatterns = [
    path('setups/', commission_setups, name='setups'),
    path('', all, name='all'),
    path('generated/', generated, name='generated'),
    path('confirmed/', confirmed, name='confirmed'),
    path('approved/', approved, name='approved'),
    path('canceled/', canceled, name='canceled'),
]
