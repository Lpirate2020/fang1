# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-04-13 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0012_auto_20210413_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicattributes',
            name='area',
            field=models.CharField(default='', max_length=10, verbose_name='房源面积'),
        ),
    ]
