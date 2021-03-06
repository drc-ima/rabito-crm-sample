# Generated by Django 3.2.6 on 2021-08-23 09:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
                'db_table': 'answer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Pending'), (2, 'Published'), (3, 'Unpublished')], null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedbacks',
                'db_table': 'feedback',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FeedbackResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(blank=True, max_length=100, null=True)),
                ('officer_id', models.CharField(blank=True, max_length=100, null=True)),
                ('feedback_code', models.CharField(blank=True, max_length=100, null=True)),
                ('is_submitted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Feedback Response',
                'verbose_name_plural': 'Feedback Responses',
                'db_table': 'feedback_response',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_code', models.CharField(blank=True, max_length=100, null=True)),
                ('text', models.CharField(blank=True, max_length=300, null=True)),
                ('question_type', models.CharField(blank=True, choices=[('Radio', 'Radio'), ('Scale', 'Scale'), ('Rating', 'Rating'), ('Fill', 'Fill'), ('Choice', 'Choice')], max_length=300, null=True)),
                ('scale_start_text', models.CharField(blank=True, max_length=300, null=True)),
                ('scale_middle_text', models.CharField(blank=True, max_length=300, null=True)),
                ('scale_end_text', models.CharField(blank=True, max_length=300, null=True)),
                ('scale_count', models.IntegerField(blank=True, null=True)),
                ('choice_answer_one', models.CharField(blank=True, max_length=300, null=True)),
                ('choice_answer_two', models.CharField(blank=True, max_length=300, null=True)),
                ('choice_answer_three', models.CharField(blank=True, max_length=300, null=True)),
                ('choice_answer_four', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'db_table': 'question',
                'managed': True,
            },
        ),
    ]
