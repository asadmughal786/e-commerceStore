# Generated by Django 4.2.4 on 2023-11-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0009_cartorders_payment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorderitems',
            name='product_id',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
