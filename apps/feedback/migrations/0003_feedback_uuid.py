# Generated by Django 3.2.6 on 2021-08-25 21:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
