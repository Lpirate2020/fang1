# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-04-13 03:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0002_auto_20210413_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicattributes',
            name='BA_state',
            field=models.IntegerField(verbose_name='房源描述'),
        ),
    ]
