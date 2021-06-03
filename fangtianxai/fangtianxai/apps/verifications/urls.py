# @Time : 2021/3/16 9:04 
# @Author : Lpirate
# @File : urls.py 
# @Software: PyCharm
from django.conf.urls import url
from . import views

urlpatterns = [
    # 发短信
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),  # 正则：第一位是1第二位3-9，后匹配9位数
]
