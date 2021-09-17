from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    # path('', user_login, name='login'),
    path('dashboard', dashboard, name='dashboard'),
    path('branches/', branches, name='branches'),
    path('roles/', roles, name='roles'),
    path('add-role/', add_role, name='add-role'),
    path('all-users/', all_users, name='all-users'),
    path('marketers/', marketer_users, name='marketers'),
    path('partners/', partner_users, name='partners'),
    path('admins/', admin_users, name='admins'),
    path('add-user/', add_user, name='add-user'),
    path('coupons/', coupons, name='coupons'),
    path('update-role/<id>/', update_role, name='update-role'),
]

handler404 = page_not_found
handler500 = server_error
handler403 = http_forbidden
handler400 = bad_request
