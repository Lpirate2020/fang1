# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-04-13 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0006_auto_20210413_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicattributes',
            name='floor',
            field=models.CharField(max_length=20, verbose_name='楼层'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='structure',
            field=models.IntegerField(choices=[(1, '平层'), (2, '复式'), (3, '错层'), (4, '跃层'), (5, '暂无数据')], max_length=1, verbose_name='户型结构'),
        ),
    ]