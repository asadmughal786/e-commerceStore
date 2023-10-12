# Generated by Django 4.2.4 on 2023-10-08 10:57

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0002_rename_images_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='specification',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='No description', null=True),
        ),
    ]