# Generated by Django 3.2.6 on 2021-09-19 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commission', '0003_auto_20210918_2319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commissionstatus',
            old_name='coupon',
            new_name='commission',
        ),
    ]
