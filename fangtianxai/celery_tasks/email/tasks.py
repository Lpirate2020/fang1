# @Time : 2021/3/22 12:34 
# @Author : Lpirate
# @File : tasks.py 
# @Software: PyCharm
from celery_tasks.main import celery_app
from django.core.mail import send_mail
from django.conf import settings


# 异步发送邮件任务
# 注册邮件
@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    """
     发送验证邮箱邮件
     :param to_email: 收件⼈邮箱
     :param verify_url: 验证链接
     :return: None
     """
    subject = "房天下邮箱验证"  # 邮件标题
    html_message = '<p>尊敬的⽤户您好！</p>' \
                   '<p>感谢您使房天下二手房交易网站。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)
    # send_mail(subject：标题, message：邮件正文, from_email：发送人, recipient_list：收件人列表,html_message：多媒体内容即超文本邮件内容):


# 给中介发邮件
@celery_app.task(name='send_to_agent')
def send_to_agent(receiver, place, mobile):
    """
    :param mobile: 联系方式
    :param place: 地址
    :param receiver: 联系人
    :return: None
    """
    print(receiver, place, mobile)
    to_email = '546038114@qq.com'
    subject = "有用户查看房源信息"  # 邮件标题
    html_message = '<p>客服您好！</p>' \
                   '<p>有用户查看房源信息</p>' \
                   '<p>联系人：'+receiver+'</p>' \
                   '<p>用户地址为：'+place+'</p>' \
                   '<p>用户联系方式为：'+mobile+'</p>' \
                   '<p>请您注意保护用户隐私，联系用户</p>'

    send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)
