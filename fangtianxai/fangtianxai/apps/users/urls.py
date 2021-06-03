# @Time : 2021/3/16 22:08 
# @Author : Lpirate
# @File : urls.py 
# @Software: PyCharm

from django.conf.urls import url
from rest_framework import routers

from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # 注册用户
    url(r'^users/$', views.UserViews.as_view()),
    # 判断用户名是否存在
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UserCountView.as_view()),
    # ?(<username>\w{5,20})正则匹配5~20个字母数字下划线

    # 判断手机号是否存在
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),

    # JWT登录
    url(r'^authorizations/$', obtain_jwt_token),

    # 获取用户详情
    url(r'^user/$', views.UserDetailView.as_view()),
    # 更新邮箱
    url(r'^email/$', views.EmailView.as_view()),

    # 更新邮箱
    url(r'^emails/verification/$', views.EmaiVerifyView.as_view()),
    # 用户更改密码
    url(r'^password/$', views.UpdatePassWord.as_view()),

]
# 联系人地址更新
router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, base_name='addresses')
urlpatterns += router.urls