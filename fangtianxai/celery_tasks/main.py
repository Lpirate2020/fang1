# @Time : 2021/3/16 19:24 
# @Author : Lpirate
# @File : main.py 
# @Software: PyCharm

# 启动文件
# 工程目录下运行celery -A celery_tasks.main worker -l info   A添加 -l显示工作日志
from celery import Celery
import os

# celery使用django中的配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fangtianxai.settings.dev")

# 1、创建celery实例
celery_app = Celery('fangtianxia')

# 2、加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 3、自动注册异步任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'send_verify_email.email','send_to_agent.email'])
