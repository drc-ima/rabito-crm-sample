# Generated by Django 3.2.6 on 2021-08-23 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='planner',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='planners', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='planner',
            name='group',
            field=models.ManyToManyField(blank=True, related_name='group_planner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='planner',
            name='joint_with',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='joint_with_planner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='planner',
            name='reschedule_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reschedule_planners', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='engagement',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='engagements', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='engagement',
            name='planner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='planner_engagement', to='schedule.planner'),
        ),
        migrations.AddField(
            model_name='comment',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
