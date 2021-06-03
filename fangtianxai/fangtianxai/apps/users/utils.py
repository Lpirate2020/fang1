# @Time : 2021/3/19 15:59 
# @Author : Lpirate
# @File : utils.py 
# @Software: PyCharm


from django.contrib.auth.backends import ModelBackend
import re
from .models import User


# 重写登录响应，原本只返回token值，需要添加用户名和id
def jwt_response_payload_handler(token, user=None, request=None):
    """重写JWT登录视图的构造响应数据函数，多追加id和username"""
    # print('xxxx')
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username,
    }


# 动态获取user
def get_user_by_account(account):
    """
    通过传入的账号动态获取user模型对象
    :param account:可能是手机号和用户名
    :return:user或none
    """
    try:
        if re.match(r'1[3-9]\d{9}$', account):  # 判断是不是手机号
            user = User.objects.get(mobile=account)  # 手机号验证
        else:
            user = User.objects.get(username=account)  # 用户名验证
    except User.DoesNotExist:
        return None
    else:
        return user

class UsernameModelAuthBackend(ModelBackend):
    """修改django认证类，实现多账户登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 获取user
        user = get_user_by_account(username)
        # 判断前端传入的密码是否正确
        if user and user.check_password(password):

            # 返回user
            return user