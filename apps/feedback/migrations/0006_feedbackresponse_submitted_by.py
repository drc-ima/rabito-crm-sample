# Generated by Django 3.2.6 on 2021-09-13 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_feedbackresponse_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackresponse',
            name='submitted_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
