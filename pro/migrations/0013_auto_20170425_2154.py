# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-25 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro', '0012_auto_20170425_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='btn_type',
            field=models.CharField(default=None, max_length=50, verbose_name='Napis na gumbu'),
        ),
    ]
