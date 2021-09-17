from apps.partner.models import Coupon, CouponStatus, Partner
from django.contrib import admin

# Register your models here.
admin.site.register(Partner)
admin.site.register(Coupon)
admin.site.register(CouponStatus)