from django.shortcuts import render
# from rest_framework.response import Response  # 响应模块
# from rest_framework import status  # 状态码模块
from rest_framework.decorators import action

from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView  # 导入数据库使用模块
from .serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer, \
    UserAddressSerializer, AddressTitleSerializer  # 导入手写的注册序列化器

from rest_framework.views import APIView
from .models import User, Address
from rest_framework.response import Response
# 状态码
from rest_framework import status
# 用户详细信息
from rest_framework.permissions import IsAuthenticated
# 地址查看
from rest_framework.viewsets import GenericViewSet

from rest_framework.mixins import UpdateModelMixin

from django.contrib.auth.hashers import make_password, check_password  # 手动验证密码


# Create your views here.

class UserViews(CreateAPIView):  # 只创建不做其他操作
    """
    用户注册视图
    """
    # 指定序列化器，只做新增操作
    serializer_class = CreateUserSerializer

    # # 导入GenericAPIView需要写的代码：
    # def post(self, request):
    #     # 创建虚拟化器
    #     serializer = self.get_serializer(data=request.data)
    #     # 拦截错误
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # # 原始代码
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


#     综上 直接导入CreateAPIView，指定序列化器 完事

class UserCountView(APIView):
    """判断用户名是否注册"""

    def get(self, request, username):  # 以url传输用户名
        # 查询user表
        count = User.objects.filter(username=username).count()  # 过滤数据库中用户名count取次数，大于一说明存在
        # 包装响应数据
        data = {
            'username': username,
            'count': count,
        }
        # print(data)
        # 响应
        return Response(data)


class MobileCountView(APIView):
    """判断手机号是否注册"""

    def get(self, request, mobile):  # 以url传输手机号
        # 查询user表
        count = User.objects.filter(mobile=mobile).count()  # 过滤数据库中用户名count取次数，大于一说明存在
        # 包装响应数据
        data = {
            'username': mobile,
            'count': count,
        }
        # print(data)
        # 响应
        return Response(data)


# 用户信息展示GET /user/
class UserDetailView(RetrieveAPIView):
    """用户详细信息展示"""
    serializer_class = UserDetailSerializer  # 序列化器
    queryset = User.objects.all()  # 指定查询集
    parser_classes = [IsAuthenticated]  # 指定权限，只有通过认证的用户才能访问当前视图

    def get_object(self):
        """重写此方法返回要展示用户的模型对象，减少对于数据库的查询"""
        return self.request.user


# 更新用户邮箱PUT /email/
class EmailView(UpdateAPIView):
    """更新用户邮箱"""
    permission_classes = [IsAuthenticated]  # 指定权限，只有通过认证的用户才能访问当前视图
    serializer_class = EmailSerializer

    def get_object(self):
        return self.request.user


# 激活邮箱请求 GET
class EmaiVerifyView(APIView):
    """# 激活邮箱请求 获取结尾的token值解密，取到user的id和邮箱，在数据库中查询，更改用户的email_active"""

    def get(self, request):
        # 获取前端查询字符串中传入的token
        token = request.query_params.get('token')
        # 解密token,并查询对应user
        user = User.check_verify_email_token(token)  # User中的静态方法
        # 修改当前user的email_active为True
        if user is None:  # token过期
            return Response({'message': '激活失败'}, status=status.HTTP_400_BAD_REQUEST)
        user.email_active = True
        user.save()
        # 响应
        return Response({'message': 'ok'})


# 用户联系地址
class AddressViewSet(UpdateModelMixin, GenericViewSet):
    """用户联系地址增删改查"""
    # 添加权限，登录用户才能添加
    permission_classes = [IsAuthenticated]
    # 指定序列化器
    serializer_class = UserAddressSerializer

    # 指定查询集
    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)  # 逻辑删除不为真
        # return Address.objects.filter(is_deleted=False)

    #     以上两者区别：前者只返回前端发回的用户的地址模型中过滤逻辑删除为假的数据，
    #     addresses小写是因为User模型与Address模型关联，addresses默认名字为user_set
    #     后者返回地址模型中所有逻辑删除为假数据

    def create(self, request):
        user = request.user  # 获取当前请求用户
        # count = user.addresses.all().count()  # 取该用户下的地址数量 user.addresses：user与address关联；.all()：取所有；.count()取数量 1对多
        count = Address.objects.filter(user=user).count()  # 通过地址模型，过滤出与该用户匹配的地址 关联过滤查询
        # 设置上限5个地址
        if count >= 5:
            return Response({'message': '联系地址数量上限'}, status=status.HTTP_400_BAD_REQUEST)

        # 新增
        # 创建序列化器进行反序列化
        serializer = self.get_serializer(data=request.data)
        # 调用序列化器的is_vaild()校验
        serializer.is_valid(raise_exception=True)
        # 调用序列化器save()存储
        serializer.save()
        # 响应
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # GET /addresses/
    def list(self, request, *args, **kwargs):
        """
        用户地址列表数据
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': 5,
            'addresses': serializer.data,
        })

    # delete /addresses/<pk>/
    # 逻辑删除
    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # put /addresses/pk/title/
    # 需要请求体参数 title 单独修改标题
    @action(methods=['put'], detail=True)
    # 装饰器的意义，路由只有增删改查的路由，其他参数路由需要自定义，detail=True表示将参数放到url之后传值
    def title(self, request, pk=None):
        """
        修改标题
        """
        address = self.get_object()
        serializer = AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # put /addresses/pk/status/
    # 设置默认地址
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


# 用户密码更改
class UpdatePassWord(APIView):
    # 添加权限，登录用户才能添加
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # 获取参数
        user_id = request.data["user_id"]  # yonghuID
        ipassword = request.data["ipassword"]  # 原始密码
        password = request.data["password"]  # 更改密码
        password2 = request.data["password2"]  # 确认密码

        # 获得请求用户
        user = User.objects.get(id=user_id)
        # print(user.password)
        # print(check_password('jkljkl1123', user.password))
        # 效验新密码是否符合要求
        if password != password2:
            raise Exception("两次密码输入不一致！")
        if len(password) > 20 or len(password) < 8:
            raise Exception("密码长度需要8到20位")

        # 检查原始密码是否正确
        if user.check_password(ipassword) == True:
            # print(1)
            # 修改密码为新密码
            user.set_password(password)
            # 保存
            user.save()
            # 返回数据
            return Response({'message': 'OK'}, status=status.HTTP_202_ACCEPTED)
        else:
            # print(2)
            return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
