from apps.commission.models import Commission, CommissionSetup, CommissionStatus
from django.contrib import admin

# Register your models here.
admin.site.register(CommissionSetup)
admin.site.register(Commission)
admin.site.register(CommissionStatus)