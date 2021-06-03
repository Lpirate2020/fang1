# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-04-13 08:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0008_auto_20210413_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailedProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inside_area', models.CharField(max_length=15, verbose_name='套内面积')),
                ('building_type', models.IntegerField(choices=[(1, '板楼'), (2, '塔楼'), (3, '平房'), (4, '板塔结合'), (5, '暂无数据')], max_length=1, verbose_name='建筑类型')),
                ('proportion', models.CharField(max_length=15, verbose_name='梯户比例')),
                ('lift', models.IntegerField(choices=[(0, '无'), (1, '有'), (2, '暂无数据')], max_length=1, verbose_name='是否配备电梯')),
                ('DP_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='house.BasicAttributes')),
            ],
            options={
                'verbose_name': '房屋详细信息',
                'verbose_name_plural': '房屋详细信息',
                'db_table': 'tb_house_detailed',
            },
        ),
    ]
