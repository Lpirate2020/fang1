"""fangtianxai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^list/$', views.ListView),  # 房源浏览
    url(r'^list_region/$', views.ListRegionView),  # 地区房源浏览

    url(r'^detail/$', views.Detail),  # 房源详细信息

    # url(r'^calculationAfter$', views.resultsData),
    url(r'^LoginSuccess/$', views.LoginSuccess),  # 用户登录成功信息写入redis
    url(r'^test/$', views.test),  # 用户登录成功信息返回vue
    url(r'^User_Redis_Del/$', views.User_Redis_Del),  # 用户登录成功信息清空redis

    url(r'^emailto/$', views.EmailToAgent),  # 给中介发邮件

]
