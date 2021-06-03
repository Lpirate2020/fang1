from django.shortcuts import render
from rest_framework.views import APIView  #
from .models import Area  # 导入省市区模型
from rest_framework.response import Response  # 响应
from rest_framework import status  # 响应状态码

from .serializer import AreaSerializers, SubsSerializer  # AreaSerializers:省序列化器,SubsSerializer:详情视图

# 优化库
# from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView

# 最终使用库
from rest_framework.viewsets import ReadOnlyModelViewSet  # ReadOnlyModelViewSet中包含RetrieveAPIView和ListModelMixin

# 省市区缓存
from rest_framework_extensions.cache.mixins import CacheResponseMixin


# Create your views here.
# # 省视图
# class AreaListView(APIView):
#     """查询所有省"""
#
#     def get(self, request):
#         # 1、获取指定查询集
#         province = Area.objects.filter(parent=None)
#         # 2、创建序列化器序列化数据
#         serializer = AreaSerializers(province, many=True)  # province是个查询集需要配置many=True
#         # 3、响应
#         return Response(serializer.data)
#
#
# # 单一查询视图
# class AreaDetailView(APIView):
#     """查询单一省或市"""
#
#     def get(self, request, pk):
#         # 1、根据PK查询出指定的省或市
#         try:  # id可能不存在
#             area = Area.objects.get(id=pk)
#         except Area.DoesNotExist:
#             return Response({'message': '无效主键'},status=status.HTTP_400_BAD_REQUEST)
#         # 2、创建序列化器序列化
#         serializer = SubsSerializer(area)
#         # 3、响应
#         return Response(serializer.data)

# # 优化
# # class AreaListView(ListModelMixin,GenericAPIView):>>>直接用ListAPIView替换
#
# class AreaListView(ListAPIView):
#     """查询所有省"""
#     # 指定序列化器
#     serializer_class = AreaSerializers
#     # 指定查询集
#     queryset = Area.objects.filter(parent=None)
#
#     # def get(self, request):
#     #     # ListModelMixin中有以下所有部分
#     #     #     # 1、获取指定查询集
#     #     #     province=self.get_queryset()
#     #     #     # 2、创建序列化器序列化数据
#     #     #     serializer =self.get_serializer(province,many=True)
#     #     #     # 3、响应
#     #     #     return Response(serializer.data)
#     #
#     #     return self.list(request)
#
#
# # 单一查询视图
# class AreaDetailView(RetrieveAPIView):
#     """查询单一省或市"""
#     # 指定序列化器
#     serializer_class = SubsSerializer
#     # 指定查询集
#     queryset = Area.objects.all()
#
#     # def get(self, request, pk):
#     #     # 1、根据PK查询出指定的省或市
#     #     try:  # id可能不存在
#     #         area = Area.objects.get(id=pk)
#     #     except Area.DoesNotExist:
#     #         return Response({'message': '无效主键'},status=status.HTTP_400_BAD_REQUEST)
#     #     # 2、创建序列化器序列化
#     #     serializer = SubsSerializer(area)
#     #     # 3、响应
#     #     return Response(serializer.data)

# 由于AreaListView与AreaDetailView流程相同，可以合并两个类视图
# 发送的都是get请求，因此需要使用视图集
class AreaViewSet(CacheResponseMixin,ReadOnlyModelViewSet):
    # CacheResponseMixin放前面表示先使用缓存中的值

    # 指定序列化器
    # 重写def get_queryset(self):判断路由后是否接值，没有则是省（多）查询，有则是下级（单一）查询
    def get_queryset(self):
        if self.action == 'list':  # 路由没有后接pk
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()

    # 指定查询集
    def get_serializer_class(self):
        if self.action == 'list':  # 路由没有后接pk
            return AreaSerializers
        else:
            return SubsSerializer

