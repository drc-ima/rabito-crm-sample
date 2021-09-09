from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

STATUS = [
    (1, 'Generated'),
    (2, 'Approved'),
    (3, 'Cancelled'),
]

class Commission(models.Model):
    partner_code = models.CharField(max_length=100, blank=True, null=True)
    patient_id = models.CharField(max_length=100, blank=True, null=True)
    coupon_code = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    status = models.IntegerField(choices=STATUS, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="commissions", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="modified_commissions", on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.amount)
    

    class Meta:
        db_table = 'commission'
        managed = True
        verbose_name = 'Commission'
        verbose_name_plural = 'Commissions'


COMMISSION_TYPES = [
    ('Flat', 'Flat'),
    ('Percent', 'Percent')
]


class CommissionSetup(models.Model):
    branch_code = models.CharField(max_length=100, blank=True, null=True)
    commission_type = models.CharField(max_length=100, blank=True, null=True, choices=COMMISSION_TYPES)
    figure = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="commission_setups", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="modified_commission_setups", on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.figure)

    class Meta:
        db_table = 'commission_setup'
        managed = True
        verbose_name = 'Commission Setup'
        verbose_name_plural = 'Commission Setups'