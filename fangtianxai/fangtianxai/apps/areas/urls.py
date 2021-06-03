# @Time : 2021/3/23 12:24 
# @Author : Lpirate
# @File : urls.py 
# @Software: PyCharm
from django.conf.urls import url
from . import views

# 创建路由

# urlpatterns = [
#     # 查询所有省
#     url(r'^areas/$', views.AreaListView.as_view()),
#     url(r'^areas/(?P<pk>\d+)/$', views.AreaDetailView.as_view()),
# ]

# 新建路由
from rest_framework.routers import DefaultRouter

urlpatterns = [
]
routers = DefaultRouter()
routers.register(r'areas', views.AreaViewSet, base_name='area')
# base_name在view中没有给queryset类属性指定查询集时需要传值，不传默认以查询集queryset中指定的查询集模型名小写作为路由别名
urlpatterns += routers.urls
