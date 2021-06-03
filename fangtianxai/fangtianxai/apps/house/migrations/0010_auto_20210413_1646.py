# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-04-13 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0009_detailedproperties'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicattributes',
            name='BA_state',
            field=models.IntegerField(choices=[(1, '入库'), (2, '停止交易'), (3, '可以交易')], max_length=1, verbose_name='房源状态'),
        ),
    ]
