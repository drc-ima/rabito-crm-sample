# Generated by Django 3.2.6 on 2021-08-23 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_patient_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='branch_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='branch_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
