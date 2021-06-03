# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-04-13 02:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailedProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inside_area', models.CharField(max_length=15)),
                ('building_type', models.CharField(max_length=15)),
            ],
        ),
        migrations.AlterModelOptions(
            name='basicattributes',
            options={'verbose_name': '房屋基本信息', 'verbose_name_plural': '房屋基本信息'},
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='BA_change_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='BA_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='标准ID'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='BA_time',
            field=models.DateTimeField(auto_now=True, verbose_name='入库时间'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='agent_name',
            field=models.CharField(max_length=5, verbose_name='经纪人'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='choices',
            field=models.CharField(choices=[(1, '0室0厅0厨0卫'), (2, '1室1厅1厨1卫'), (3, '2室1厅1厨1卫'), (4, '2室2厅1厨1卫'), (5, '3室2厅1厨1卫'), (6, '3室2厅1厨2卫'), (7, '3室1厅1厨1卫'), (8, '2室0厅1厨1卫'), (9, '1室0厅1厨1卫'), (10, '1室2厅1厨1卫'), (11, '4室2厅1厨2卫'), (12, '4室1厅1厨4卫'), (13, '2室2厅1厨2卫'), (14, '5室2厅1厨2卫'), (15, '2室1厅1厨2卫'), (16, '3室1厅1厨2卫'), (17, '3室0厅1厨1卫'), (18, '5室3厅1厨2卫'), (19, '4室1厅1厨1卫'), (20, '4室2厅2厨2卫'), (21, '3室2厅1厨3卫'), (22, '5室1厅1厨1卫'), (23, '1室0厅0厨1卫'), (24, '6室4厅2厨3卫'), (25, '4室2厅1厨5卫'), (26, '5室2厅1厨3卫')], max_length=8, verbose_name='户型'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='decoration',
            field=models.CharField(max_length=2, verbose_name='装修情况'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='floor',
            field=models.CharField(max_length=20, verbose_name='楼层'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='name',
            field=models.CharField(max_length=200, verbose_name='房源描述'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='orientation',
            field=models.CharField(max_length=10, verbose_name='房屋朝向'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='price',
            field=models.FloatField(max_length=10, verbose_name='房源价格'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='price_m',
            field=models.FloatField(max_length=10, verbose_name='每平米价格'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='structure',
            field=models.CharField(choices=[(1, '平层'), (2, '复式'), (3, '错层'), (4, '跃层'), (5, '暂无数据')], max_length=5, verbose_name='户型结构'),
        ),
        migrations.AddField(
            model_name='detailedproperties',
            name='DP_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.BasicAttributes'),
        ),
    ]
