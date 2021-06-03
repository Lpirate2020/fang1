from django.shortcuts import render
from rest_framework.views import APIView
from random import randint  # 随机整数生成验证码
from django_redis import get_redis_connection  # redis缓存数据
from fangtianxai.libs.yuntongxun.sms import CCP  # 使用容联云通讯发验证码

from rest_framework.response import Response  # 制作响应

import logging  # 打印信息
from rest_framework import status  # 导入状态码
from . import constants  # 导入常量集
from celery_tasks.sms.tasks import send_sms_code  # 导入异步任务队列

logger = logging.getLogger('django')


# Create your views here.
class SMSCodeView(APIView):
    """短信验证码"""

    # 使用get传输接收电话号码
    def get(self, request, mobile):
        # 1、创建redis连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 2、从redis中先获取发送标记
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        # 3、如果取出标记，说明频繁发送标记
        if send_flag:
            return Response({'message': '手机频繁发送短信验证码'}, status=status.HTTP_400_BAD_REQUEST)

        # 优化：send_flag，redis_conn.setex*2，一共需要使用连接三次redis数据库，使用管道技术进行优化
        # 创建redis管道，把多次redis操作将来一次性去执行，减少redis连接操作
        pl = redis_conn.pipeline()
        # 发短信流程
        # 4、生成验证码
        sms_code = '%06d' % randint(0, 999999)  # '%06d'打印6个字符不足用0补齐
        logger.info(sms_code)

        # 5、把验证码存储到redis中
        # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)#原始访问redis
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)  # 语句塞入管道
        # setex保存为字符串格式，'sms_%s'%mobile键,300过期时间，sms_code值

        # 5.1、存储标记，表示此手机号以发送过短信，标记有效期60s
        # redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)  # 原始访问redis
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)  # 语句塞入管道
        # 1作为标记eg：{send_flag_18334068851:1}

        # 执行管道
        pl.execute()

        # 6、利用容联云通讯发送短信验证码
        # CCP().send_template_sms(self, 目标手机号, 列表：验证码，过期时间（5分钟）, 模板)
        # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
        # 触发异步任务，将异步任务添加到celery任务队列
        # send_sms_code(mobile, sms_code)#这样的话只是将上面的语句换了个库运行
        send_sms_code.delay(mobile, sms_code)  # 触发异步任务

        # 7、响应
        return Response({'message': 'ok'})
