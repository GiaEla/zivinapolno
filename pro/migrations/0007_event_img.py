# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-25 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pro', '0006_auto_20170422_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='img',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pro.Image', verbose_name='slika'),
        ),
    ]
