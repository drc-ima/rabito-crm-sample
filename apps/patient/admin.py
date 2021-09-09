from apps.patient.models import Attendance, Patient
from django.contrib import admin

# Register your models here.

admin.site.register(Patient)
admin.site.register(Attendance)