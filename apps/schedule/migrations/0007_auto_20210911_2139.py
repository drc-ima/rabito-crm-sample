# Generated by Django 3.2.6 on 2021-09-11 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20210909_2052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='engagement',
            options={'managed': True, 'ordering': ('-created_at',), 'verbose_name': 'Engagement', 'verbose_name_plural': 'Engagements'},
        ),
        migrations.AddField(
            model_name='planner',
            name='original_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='planner',
            name='original_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='planner',
            name='orignal_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
