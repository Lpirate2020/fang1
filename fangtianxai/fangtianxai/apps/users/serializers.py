# @Time : 2021/3/16 22:13 
# @Author : Lpirate
# @File : serializers.py 
# @Software: PyCharm

from rest_framework import serializers
from .models import User, Address  # 映射数据库模型
import re
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings

from celery_tasks.email.tasks import send_verify_email  # 异步发送邮件


class CreateUserSerializer(serializers.ModelSerializer):  # ModelSerializer自动映射生成
    """注册序列化器"""
    # 序列化器需的所有字段：['id','username','password','password2','mobile','sms_code','allow']
    # 需要校验的字段：['username','password','password2','mobile','sms_code','allow']
    # 模型中存在的字段：['username','password','mobile',]
    # 'sms_code','allow'需要自己定义

    # 需要序列化数据：['id','password','mobile',]
    # 需要反序列化的数据：['username','password','password2','mobile','sms_code','allow']

    password2 = serializers.CharField(label='确认密码', write_only=True)  # 只做反序列化
    sms_code = serializers.CharField(label='验证码', write_only=True)  # 只做反序列化
    allow = serializers.CharField(label='同意协议', write_only=True)  # 只做反序列化 前端返回：'true'
    token = serializers.CharField(label='token', read_only=True)  # 只做反序列化  建立token实现jwt

    class Meta:
        model = User  # 从User模型中映射序列化器字段
        # 指定映射部分
        # fields = '__all__'#映射全部
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow',
                  'token']  # 设置映射字段，额外添加'token'

        extra_kwargs = {  # 修改字段选项
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的⽤户名',  # 反序列化校验出错信息
                    'max_length': '仅允许5-20个字符的⽤户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 反序列化校验
    # 校验前端数据，后端需要再度校验前端数据
    def validate_mobile(self, vlue):
        """单独校验手机号"""
        if not re.match(r'1[3-9]\d{9}$', vlue):  # 如果校验出错
            raise serializers.ValidationError('手机号格式有误')
        return vlue  # 抛出异常

    def validate_allow(self, vlue):
        """单独校验是否同意协议"""
        # print(vlue)
        if vlue != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return vlue

    def validate(self, attrs):  # attrs前端传来的全部数据
        """联合校验俩密码是否正确"""
        print(attrs)
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')

        # 校验验证码
        redis_conn = get_redis_connection('verify_codes')  # 取redis中的验证码
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)  # 此时可能过了五分钟有效期
        # 注：向redis中存储时都是以字符串形式存储，取出后都是bytes类型
        # real_sms_code.decode(),且以下判断不可逆，因为如果real_sms_code为none时无法.decode()程序会报错
        if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():  # 验证码过期或者前端验证码与redis中不相同
            raise serializers.ValidationError('验证码错误')

        return attrs

    def create(self, validated_data):
        """重写create存储对应数据"""
        # 移除以下三个不需要存储的属性
        # print(validated_data)
        del validated_data['password2']  # 确认密码不存
        del validated_data['sms_code']  # 验证码不存
        del validated_data['allow']  # 同意协议不存

        # 弹出password值
        password = validated_data.pop('password')
        # 创建用户模型，给模型中的password和mobile赋值
        user = User(**validated_data)
        user.set_password(password)  # 加密密码后再赋值给password属性
        user.save()  # 存入数据库

        # 创建token作为返回
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用jwt_payload_handler生成payload载荷
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 生成jwt

        payload = jwt_payload_handler(user)  # 根据user消息返回相关载荷
        token = jwt_encode_handler(payload)  # 传入载荷生成jwt
        user.token = token  # token默认5分钟300秒过期

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'email_active']  # 设置映射字段


class EmailSerializer(serializers.ModelSerializer):
    """更新邮箱序列化器"""

    class Meta:
        model = User
        fields = ['id', 'email']  # 设置映射字段
        extra_kwargs = {
            # 修改模型中email反序列化时可以为空，修改为'required': True,表示反序列化校验是必须要传值
            'email': {
                'required': True
            }
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')  # instance==user的模型
        instance.save()

        # 发送邮件功能
        verify_url = instance.generate_email_verify_url()  # models中生成激活邮箱连接
        # 异步发送邮件：新建发送包
        # http://www.fangtianxia.site:8080/success_verify_email.html?token=''
        send_verify_email.delay(instance.email, verify_url=verify_url)  # verify_url激活链接
        return instance


class UserAddressSerializer(serializers.ModelSerializer):
    """
    ⽤户地址序列化器
    """
    province = serializers.StringRelatedField(read_only=True)  # 省
    city = serializers.StringRelatedField(read_only=True)  # 市
    district = serializers.StringRelatedField(read_only=True)  # 区
    # 以上三个字段在模型中是外键，在这里定义是不使用外键定义的值

    province_id = serializers.IntegerField(label='省ID', required=True)  # required=True反序列化输入时使用
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)

    class Meta:
        model = Address

        exclude = ('user', 'is_deleted', 'create_time', 'update_time')  # 排除外键，逻辑删除，创建时间，更新时间

    def validate_mobile(self, value):
        """
        验证⼿机号
        """
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('⼿机号格式错误')
        return value

    def create(self, validated_data):
        # 获取用户模型
        user = self.context['request'].user  # 这种取值需要父类是GenericAPIView或其子类
        # 将用户模型保存到字典中
        validated_data['user'] = user
        return Address.objects.create(**validated_data)


class AddressTitleSerializer(serializers.ModelSerializer):
    """
    地址标题
    """

    class Meta:
        model = Address
        fields = ('title',)
