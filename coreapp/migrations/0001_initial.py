# Generated by Django 4.2.4 on 2023-08-24 14:10

import coreapp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('cid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdef12345', length=10, max_length=30, prefix='cat', unique=True)),
                ('image', models.ImageField(null=True, upload_to='Category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
            managers=[
                ('cat', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('prod_image', models.ImageField(blank=True, default='static/img/logo.png', null=True, upload_to=coreapp.models.Product.product_image_path)),
                ('pid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdef12345', length=10, max_length=30, prefix='scat', unique=True)),
                ('title', models.CharField(default='New Product', max_length=100)),
                ('specification', models.TextField(blank=True, default='No description', null=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('qty', models.PositiveIntegerField(default=0)),
                ('warrenty', models.CharField(blank=True, max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=99999999999999999999)),
                ('old_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=99999999999999999999)),
                ('product_status', models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('rejected', 'Rejected'), ('in_review', 'In Review'), ('publish', 'Published')], default='in_review', max_length=10)),
                ('status', models.BooleanField(default=True)),
                ('in_stock', models.BooleanField(default=True)),
                ('sku', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=4, max_length=20, prefix='sku', unique=True)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='coreapp.category')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
            managers=[
                ('prod', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coreapp.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Wishlist',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('ratings', models.IntegerField(choices=[('1', '★☆☆☆☆'), ('2', '★★☆☆☆'), ('3', '★★★☆☆'), ('4', '★★★★☆'), ('5', '★★★★★')], default=None)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coreapp.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Products Reviews',
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to='product-image')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coreapp.product')),
            ],
            options={
                'verbose_name_plural': 'Product Image',
            },
        ),
        migrations.CreateModel(
            name='CartOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=99999999999999999999)),
                ('payment_status', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('product_status', models.CharField(choices=[('process', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='process', max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cart Orders',
            },
        ),
        migrations.CreateModel(
            name='CartOrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=200)),
                ('item', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('qty', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=99999999999999999999)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=99999999999999999999)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreapp.cartorders')),
            ],
            options={
                'verbose_name_plural': 'Cart Ordered Items',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Address',
            },
        ),
    ]
