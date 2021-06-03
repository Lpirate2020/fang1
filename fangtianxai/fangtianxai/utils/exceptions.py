# @Time : 2021/3/15 11:26 
# @Author : Lpirate
# @File : exceptions.py 
# @Software: PyCharm
# 自定义异常--拦截mysql与redis异常
from rest_framework.views import exception_handler as drf_exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status

# 获取在配置⽂件中定义的logger，⽤来记录⽇志
logger = logging.getLogger('django')


def exception_handler(exc, context):  # 在DRX异常处理的基础上自定义拦截mysql与redis的异常
    """
    ⾃定义异常处理
    :param exc: 异常实例对象
    :param context: 抛出异常的上下⽂(包含request和view对象)
    :return: Response响应对象
    """
    # 调⽤drf框架原⽣的异常处理⽅法
    response = drf_exception_handler(exc, context)
    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):  # 判断是不是mysql或者redis数据库错误
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
            # 页面报错507，提示服务器内部错误
    return response
