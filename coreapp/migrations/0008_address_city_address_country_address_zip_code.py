# Generated by Django 4.2.4 on 2023-11-01 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0007_cartorderitems_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='address',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
