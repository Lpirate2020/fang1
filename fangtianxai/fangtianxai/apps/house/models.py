from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
"""
'房屋名称', '房屋总价格', '房屋每平米价格', '房屋户型', '所在楼层', '面积', '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况',
'梯户比例', '配备电梯', '挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限', '产权所属', '抵押信息', '房本备件', '图片存储地址', '中介名',
'房屋所在地区'
"""


class HouseInfo(models.Model):
    # 房源状态
    BA_STATE = (
        (0, '停止交易'),
        (1, '入库'),
        (2, '可以交易'),
    )
    house_id = models.AutoField(primary_key=True, verbose_name='标准ID')  # 主键id
    # BA_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')  # 获取当前时间作为入库时间
    # BA_change_time = models.DateTimeField(auto_now_add=True, verbose_name='入库时间')  # 获取当前时间作为修改时间
    house_state = models.IntegerField(choices=BA_STATE, verbose_name='房源状态')  # 房源状态

    name = models.CharField(max_length=200, verbose_name='房源描述')  # 房屋描述

    price = models.FloatField(max_length=10, verbose_name='房源价格')  # 价格
    price_m = models.FloatField(max_length=10, verbose_name='每平米价格')  # 每平米价格
    choices = models.CharField(max_length=10, verbose_name='户型')  # 户型
    floor = models.CharField(max_length=20, verbose_name='楼层')  # 楼层
    area = models.CharField(max_length=10, verbose_name='房源面积', default='')  # 房源面积
    structure = models.CharField(max_length=10, verbose_name='户型结构')  # 户型结构

    inside_area = models.CharField(max_length=15, verbose_name='套内面积')  # 套内面积
    building_type = models.CharField(max_length=15, verbose_name='建筑类型')  # 建筑类型
    orientation = models.CharField(max_length=10, verbose_name='房屋朝向')  # 房屋朝向
    building_structure = models.CharField(max_length=10, verbose_name='建筑结构')  # 建筑结构
    decoration = models.CharField(max_length=10, verbose_name='装修情况')  # 装修情况
    proportion = models.CharField(max_length=15, verbose_name='梯户比例')  # 梯户比例
    lift = models.CharField(max_length=10, verbose_name='是否配备电梯')  # 是否配备电梯

    listing_time = models.DateField(verbose_name='挂牌时间',auto_now_add=True)  # 挂牌时间
    transaction_type = models.CharField(max_length=15, verbose_name='交易权属')  # 交易权属
    # last_time = models.DateTimeField(verbose_name='上次交易')  # 上次交易
    purpose = models.CharField(max_length=4, verbose_name='房屋用途')  # 房屋用途
    ascription_year = models.CharField(max_length=4, verbose_name='房屋年限')  # 房屋年限
    property_right = models.CharField(max_length=10, verbose_name='产权所属')  # 产权所属
    mortgage = models.CharField(max_length=20, verbose_name='抵押信息')  # 抵押信息
    premises_permit = models.CharField(max_length=10, verbose_name='房本备件')  # 房本备件

    image_add = models.CharField(max_length=200, verbose_name='图片存储地址')  # 图片存储地址
    agent_name = models.CharField(max_length=5, verbose_name='经纪人')  # 经纪人
    region = models.CharField(max_length=10, verbose_name='地区', default='')  # 地区

    class Meta:  # 配置数据库表名及设置模型在admin站点显示的中文名
        db_table = 'house_info'
        verbose_name = '房屋信息'
        verbose_name_plural = verbose_name
