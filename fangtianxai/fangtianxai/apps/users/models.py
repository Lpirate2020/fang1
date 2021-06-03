from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData  # TJWSSerializer加密,BadData过期异常
from django.conf import settings

from fangtianxai.utils.models import BaseModel


# Create your models here.

# AbstractUser 库中没有电话验证字段需要自己重写
class User(AbstractUser):
    """自定义模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')  # 自定义电话号码验证，设置类型为char，长度为11，数据唯一
    email_active = models.BooleanField(default=False, verbose_name='邮箱激活状态')  # 自定义电邮箱激活状态
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')  # 默认地址

    class Meta:  # 配置数据库表名及设置模型在admin站点显示的中文名
        db_table = 'tb_users'
        verbose_name = '⽤户'
        verbose_name_plural = verbose_name

    def generate_email_verify_url(self):
        """生成邮箱激活连接"""
        # 1、创建加密序列化器
        serializer = TJWSSerializer(settings.SECRET_KEY, 3600 * 24)  # 加密，设置有效期一天
        # 2、调用dumps方法加密，数据是bytes类型
        data = {
            'user_id': self.id,
            'email': self.email,
        }
        token = serializer.dumps(data).decode()
        # 3、拼接激活url
        return 'http://www.fangtianxia.site:8080/success_verify_email.html?token=' + token

    # def check_verify_email_token(self, token):  # 实例方法转化为静态方法
    # check_verify_email_token实例的调用：
    # User.check_verify_email_token(user(),token) user()在本部分不使用，浪费了性能，因此转换为静态方法
    @staticmethod
    def check_verify_email_token(token):  # 实例方法转化为静态方法
        """解密token并查询user"""
        # 1、创建加密序列化器
        serializer = TJWSSerializer(settings.SECRET_KEY, 3600 * 24)  # 加密，设置有效期一天
        # 2、调用loads解密,注意token是否过期
        try:  # token可能过期
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            id = data.get('user_id')
            email = data.get('email')
            try:  # user可能查不到
                user = User.objects.get(id=id, email=email)
            except User.DoesNotExist:
                return None
            else:
                return user


class Address(BaseModel):  # BaseModel让表中有创建时间
    """
    ⽤户地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='⽤户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='联系⼈')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='⼿机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电⼦邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '⽤户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
