"""rabito_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.user.views import permission_error, user_login, user_logout
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from apps.user import urls as user_urls
from apps.patient import urls as patient_urls
from apps.feedback import urls as feedback_urls
from apps.commission import urls as commission_urls
from apps.marketer import urls as marketer_urls
from apps.schedule import urls as schedule_urls


def layout(request):
    return render(request, 'crm/layout.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm/', include(user_urls, namespace="user")),
    path('patient/', include(patient_urls, namespace="patient")),
    path('feedback/', include(feedback_urls, namespace="feedback")),
    path('commission/', include(commission_urls, namespace="commission")),
    path('marketer/', include(marketer_urls, namespace="marketer")),
    path('planner/', include(schedule_urls, namespace="schedule")),
    path('permission-error/', permission_error, name="permission-error"),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
