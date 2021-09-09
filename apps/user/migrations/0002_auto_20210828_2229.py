# Generated by Django 3.2.6 on 2021-08-28 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='region',
            field=models.CharField(blank=True, choices=[('Ahafo', 'Ahafo'), ('Ashanti', 'Ashanti'), ('Bono East', 'Bono East'), ('Brong Ahafo', 'Brong Ahafo'), ('Central', 'Central'), ('Eastern', 'Eastern'), ('Greater Accra', 'Greater Accra'), ('North East', 'North East'), ('Northern', 'Northern'), ('Oti', 'Oti'), ('Savannah', 'Savannah'), ('Upper East', 'Upper East'), ('Western', 'Western'), ('Western North', 'Western North'), ('Volta', 'Volta')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[('PU', 'Partner User'), ('MAU', 'Marketing Admin User'), ('MU', 'Marketer User'), ('AD', 'Admins')], max_length=100, null=True),
        ),
    ]