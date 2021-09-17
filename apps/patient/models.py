from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid

# Create your models here.


class Patient(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    branch_code = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="patients", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'patient'
        managed = True
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.code

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    patient_code = models.CharField(max_length=100, blank=True, null=True)
    branch_code = models.CharField(max_length=100, blank=True, null=True)
    is_first = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="attendances", on_delete=models.DO_NOTHING)
    
    class Meta:
        db_table = 'attendance'
        managed = True
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        ordering = ['-created_at']

    def __str__(self):
        return self.patient_code
    
