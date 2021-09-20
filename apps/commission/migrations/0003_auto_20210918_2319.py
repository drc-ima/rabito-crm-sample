# Generated by Django 3.2.6 on 2021-09-18 23:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commission', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commission',
            options={'managed': True, 'verbose_name': 'Commission', 'verbose_name_plural': 'Commissions'},
        ),
        migrations.AlterField(
            model_name='commission',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'Generated'), (2, 'Confirmed'), (3, 'Approved'), (4, 'Canceled')], null=True),
        ),
        migrations.CreateModel(
            name='CommissionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Generated'), (2, 'Confirmed'), (3, 'Approved'), (4, 'Canceled')], null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='commission_status_commission', to='commission.commission')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='commission_statuses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Commission Status',
                'verbose_name_plural': 'Commission Statuses',
                'db_table': 'commission_status',
                'managed': True,
            },
        ),
    ]
