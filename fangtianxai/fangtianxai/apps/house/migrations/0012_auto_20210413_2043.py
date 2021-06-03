# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-04-13 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0011_auto_20210413_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_time', models.DateTimeField(verbose_name='挂牌时间')),
                ('last_time', models.DateTimeField(verbose_name='上次交易')),
                ('transaction_type', models.IntegerField(choices=[(0, '商品房'), (1, '已购公房'), (2, '经济适用房')], verbose_name='交易权属')),
                ('purpose', models.IntegerField(choices=[(0, '普通住宅'), (1, '商业'), (2, '底商')], verbose_name='房屋用途')),
                ('ascription_year', models.IntegerField(choices=[(0, '未满两年'), (1, '满两年'), (2, '满五年'), (3, '暂无数据')], verbose_name='房屋年限')),
                ('property_right', models.IntegerField(choices=[(0, '共有'), (1, '非公有')], verbose_name='产权所属')),
                ('premises_permit', models.IntegerField(choices=[(0, '未上传房本照片'), (1, '已上传房本照片')], verbose_name='房本备件')),
                ('mortgage', models.CharField(max_length=20, verbose_name='抵押信息')),
            ],
            options={
                'verbose_name': '房屋交易信息',
                'verbose_name_plural': '房屋交易信息',
                'db_table': 'tb_house_transaction',
            },
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='BA_state',
            field=models.IntegerField(choices=[(1, '入库'), (2, '停止交易'), (3, '可以交易')], verbose_name='房源状态'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='choices',
            field=models.IntegerField(choices=[(1, '0室0厅0厨0卫'), (2, '1室1厅1厨1卫'), (3, '2室1厅1厨1卫'), (4, '2室2厅1厨1卫'), (5, '3室2厅1厨1卫'), (6, '3室2厅1厨2卫'), (7, '3室1厅1厨1卫'), (8, '2室0厅1厨1卫'), (9, '1室0厅1厨1卫'), (10, '1室2厅1厨1卫'), (11, '4室2厅1厨2卫'), (12, '4室1厅1厨4卫'), (13, '2室2厅1厨2卫'), (14, '5室2厅1厨2卫'), (15, '2室1厅1厨2卫'), (16, '3室1厅1厨2卫'), (17, '3室0厅1厨1卫'), (18, '5室3厅1厨2卫'), (19, '4室1厅1厨1卫'), (20, '4室2厅2厨2卫'), (21, '3室2厅1厨3卫'), (22, '5室1厅1厨1卫'), (23, '1室0厅0厨1卫'), (24, '6室4厅2厨3卫'), (25, '4室2厅1厨5卫'), (26, '5室2厅1厨3卫')], verbose_name='户型'),
        ),
        migrations.AlterField(
            model_name='basicattributes',
            name='structure',
            field=models.IntegerField(choices=[(1, '平层'), (2, '复式'), (3, '错层'), (4, '跃层'), (5, '暂无数据')], verbose_name='户型结构'),
        ),
        migrations.AlterField(
            model_name='detailedproperties',
            name='building_type',
            field=models.IntegerField(choices=[(1, '板楼'), (2, '塔楼'), (3, '平房'), (4, '板塔结合'), (5, '暂无数据')], verbose_name='建筑类型'),
        ),
        migrations.AlterField(
            model_name='detailedproperties',
            name='lift',
            field=models.IntegerField(choices=[(0, '无'), (1, '有'), (2, '暂无数据')], verbose_name='是否配备电梯'),
        ),
        migrations.AddField(
            model_name='transactionattribute',
            name='TA_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='house.BasicAttributes'),
        ),
    ]