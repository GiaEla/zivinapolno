# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-25 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro', '0008_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Slika'),
        ),
    ]
