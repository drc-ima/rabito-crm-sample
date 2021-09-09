from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Partner(models.Model):
    partner_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='partner', blank=True, null=True, on_delete=models.DO_NOTHING)
    workplace = models.CharField(max_length=300, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='partners', on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=100)
    branch_code = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="feedbacks", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'partner_bio'
        managed = True
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
    
    def __str__(self):
        return self.workplace


COUPON_STATUS = [
    (1, 'Generated'),
    (2, 'Admitted'),
    (3, 'Commissioned'),
    (4, 'Approved'),
    (5, 'Cancelled')
]


class Coupon(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    patient_first_name = models.CharField(max_length=100, blank=True, null=True)
    patient_last_name = models.CharField(max_length=100, blank=True, null=True)
    patient_phone_number = models.CharField(max_length=100, blank=True, null=True)
    patient_dob = models.DateField(blank=True, null=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="coupons", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=COUPON_STATUS, blank=True, null=True)
    
    class Meta:
        db_table = 'coupon'
        managed = True
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return self.code
    