from django.urls import path
from .views import *

app_name = 'partner'


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('coupons/', coupons, name='coupons'),
    path('commissions/', commissions, name='commissions'),
    path('coupons-search/', search_coupons, name='coupons_search')
]
