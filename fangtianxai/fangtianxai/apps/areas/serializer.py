# @Time : 2021/3/23 12:28 
# @Author : Lpirate
# @File : serializer.py 
# @Software: PyCharm

# 序列化器
from rest_framework import serializers
from .models import Area  # 选择映射模型

"""
逻辑：
查询所有省时AreaSerializers                                                           省不确定时
查询单一省SubsSerializer——》其中的查询所有省时AreaSerializers代表查询省下属市                省确定，省（一）对市（多）
查询单一市SubsSerializer——》其中的查询所有市时AreaSerializers代表查询省下属区                市确定，市（一）对区（多）
"""


class AreaSerializers(serializers.ModelSerializer):
    """省序列化器"""

    class Meta:
        model = Area
        fields = ['id', 'name']  # 选择映射字段


class SubsSerializer(serializers.ModelSerializer):
    """详情视图使用的序列化器----关联序列化"""
    # 调用省序列化器，输出id和name，关联序列化本体
    subs = AreaSerializers(many=True)  # many=True多对一，多的一方需要调用

    # subs = serializers.PrimaryKeyRelatedField()  # 只序列化id
    # subs = serializers.StringRelatedField()  # 序列化模型中的str方法返回值

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
        # 'id', 230000
        # 'name',黑龙江省
        # 'subs',黑龙江省下属行政区
