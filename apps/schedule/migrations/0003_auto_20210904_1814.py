# Generated by Django 3.2.6 on 2021-09-04 18:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planner',
            name='activity_type',
        ),
        migrations.RemoveField(
            model_name='planner',
            name='joint_with',
        ),
        migrations.AddField(
            model_name='planner',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
