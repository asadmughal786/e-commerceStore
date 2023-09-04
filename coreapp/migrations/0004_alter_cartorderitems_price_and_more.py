# Generated by Django 4.2.4 on 2023-09-04 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0003_alter_cartorderitems_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorderitems',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='cartorders',
            name='price',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]