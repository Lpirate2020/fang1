import json

from django.shortcuts import render
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage  # 分页模板
from django.http import HttpResponse, JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from house.models import HouseInfo
from django.db.models import Q
from django_redis import get_redis_connection  # redis缓存数据
from rest_framework import status
from django.forms.models import model_to_dict  # 查询对象转字典

from users.models import Address  # 导入用户地址

from celery_tasks.email.tasks import send_to_agent  # 导入异步发邮件


# GET /list/
# POST /list/
@csrf_exempt  # csrf豁免，post传值可能被拒绝
def ListView(request):
    """房源概览展示页"""

    # 房源总数--从数据库中查询
    count = HouseInfo.objects.filter(house_state=2).count()

    # 房源搜索
    key = request.POST.get('key')
    key0 = ""
    # 模糊查询
    # print(key)
    if key is None or key == "":
        search = HouseInfo.objects.filter(house_state=2)
    else:
        key0 = key
        search = HouseInfo.objects.filter(house_state=2).filter(
            Q(name__icontains=key)  # 名称
            # Q(price__icontains=key) |  # 价格
            # Q(area__icontains=key) |  # 面积
            # Q(price_m__icontains=key) |  # 每平米价格
            # Q(floor__icontains=key) |  # 楼层
            # Q(orientation__icontains=key)  # 房屋朝向
        )

    # 房源基础属性展示
    # house_infos = BasicAttributes.objects.filter(BA_state=3)  # 过滤房源状态为上架的房屋
    # 分页
    paginator = Paginator(search, 50)  # 创建分页对象
    # 判断当前页数
    hindex = request.GET.get("hindex")
    if hindex is None or int(hindex) > paginator.num_pages:
        hindex = 1
    else:
        hindex = int(hindex)

    page = paginator.page(hindex)

    # 获得当前时间
    now = datetime.datetime.now()
    # 转换为指定的格式:
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")

    # 1、创建redis连接对象
    redis_conn = get_redis_connection('success_user')
    # 2、获取信息
    user_remember = redis_conn.get('remember_data')  # 记住登录的用户状态
    user_none_remember = redis_conn.get('none_remember_data')  # 未记住登录的用户状态

    # redis_conn.delete('remember_data')#删除测试

    if user_remember is None:  # 记住库中值空
        if user_none_remember is None:  # 未记住库空
            '''全空'''
            return_dict = {'user_status': '库为空'}
        else:
            '''未记住不空'''
            return_dict = user_none_remember
    else:
        '''记住不空'''
        return_dict = user_remember

    return render(request, 'list.html', {"now_time": otherStyleTime,  # 当前时间
                                         "count": len(search),  # 房源数量
                                         # "house_infos": house_infos,  # 过滤的房屋基本信息 测试用
                                         "page": page,  # 分页数据 house_infos
                                         "hindex": hindex,  # 当前页数
                                         "key": key0,  # 搜索
                                         'user_redis': return_dict,  # 登录用户信息
                                         })


# GET /list_region/?region=region&hindex=hindex
# POST /list_region/?region=region
@csrf_exempt
def ListRegionView(request):
    """地区概览展示页"""

    # 地区获取
    region = request.GET.get('region')
    # print(region)

    # 房源总数
    count = HouseInfo.objects.filter(house_state=2).filter(region=region).count()
    # 房源搜索
    key = request.POST.get('key')
    # print(key)
    key0 = ""
    # 模糊查询
    # print(key)
    if key is None or key == "":
        search = HouseInfo.objects.filter(house_state=2).filter(region=region)
    else:
        key0 = key
        search = HouseInfo.objects.filter(house_state=2).filter(region=region).filter(
            Q(name__icontains=key)  # 名称
            # Q(price__icontains=key) |  # 价格
            # Q(area__icontains=key) |  # 面积
            # Q(price_m__icontains=key) |  # 每平米价格
            # Q(floor__icontains=key) |  # 楼层
            # Q(orientation__icontains=key)  # 房屋朝向
        )
        print(len(search))

    # 房源基础属性展示
    # house_infos = BasicAttributes.objects.filter(BA_state=3)  # 过滤房源状态为上架的房屋
    # 分页
    paginator = Paginator(search, 50)  # 创建分页对象
    # 判断当前页数
    hindex = request.GET.get("hindex")
    if hindex is None or int(hindex) > paginator.num_pages:  # 页码为空或者页码超出最大
        hindex = 1
    else:
        hindex = int(hindex)

    page = paginator.page(hindex)

    # 获得当前时间
    now = datetime.datetime.now()
    # 转换为指定的格式:
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'list_region.html', {"now_time": otherStyleTime,  # 当前时间
                                                "count": len(search),  # 房源数量
                                                # "house_infos": house_infos,  # 过滤的房屋基本信息 测试用
                                                "page": page,  # 分页数据 house_infos
                                                "hindex": hindex,  # 当前页数
                                                "key": key0,  # 搜索
                                                "region": region,
                                                })


# # 用户登录状态保存redis缓存
def LoginSuccess(request):
    # POST
    # 获取登录成功用户信息

    user_post_data = json.loads(request.body, encoding='utf-8')  # json类型转字典
    user_data = json.dumps(user_post_data)  # 转str类型解决redis存储问题 b"{'key':'vlue'}“这种会出错需要b’{”key“:”vlue“}‘

    # 1、判断user_status，作为是否记住登录的条件
    # 2、创建redis连接对象
    redis_conn = get_redis_connection('success_user')
    # print(user_post_data['user_status'])
    if user_post_data['user_status']:
        '''记住登录'''
        # redis_conn.delete('none_remember_data')  # 删除未记住

        # 3、存储信息
        redis_conn.set('remember_data', user_data)
        # 4、取值返回
        user_redis = redis_conn.get('remember_data')
        # 5、数据一致化
        dict_user = json.loads(user_redis)  # 转换为字典类型

        return JsonResponse({'content1': dict_user, 'msg': '错误信息'}, status=status.HTTP_200_OK)
    else:
        '''未记住登录'''
        # redis_conn.delete('remember_data')  # 删除记住

        # 3、存储信息
        redis_conn.set('none_remember_data', user_data)  # 区别
        # 4、取值返回
        user_redis = redis_conn.get('none_remember_data')
        # 5、数据一致化
        dict_user = json.loads(user_redis)  # 转换为字典类型

        return JsonResponse({'content1': dict_user, 'msg': '错误信息'}, status=status.HTTP_200_OK)


# 用户登录缓存信息获取
def test(request):
    # 1、创建redis连接对象
    redis_conn = get_redis_connection('success_user')
    # 2、获取信息
    user_remember = redis_conn.get('remember_data')  # 记住登录的用户状态
    user_none_remember = redis_conn.get('none_remember_data')  # 未记住登录的用户状态

    # redis_conn.delete('remember_data')  # 删除测试

    if user_remember is None:  # 记住库中值空
        if user_none_remember is None:  # 未记住库空
            '''全空'''
            ret_dict = {'user_status': None}
            return_dict = json.dumps(ret_dict, ensure_ascii=False)
        else:
            '''未记住不空'''
            return_dict = user_none_remember
    else:
        '''记住不空'''
        return_dict = user_remember

    # print(type(return_dict))  # bytes类型
    # print(return_dict)

    # user_redis=json.loads(return_dict) # bytes转字典
    # print(user_redis)

    return JsonResponse({'content1': json.loads(return_dict), 'msg': '错误信息'})  # 数据转换成json回传vue

    # return render(request, "test.html", {'user_redis': return_dict,  # json格式})#http://127.0.0.1:8000/test/传值测试


# 用户登录状态redis缓存删除
def User_Redis_Del(request):
    # 1、创建redis连接对象
    redis_conn = get_redis_connection('success_user')
    # 2、直接清空两个库--说是库其实是{{'remember_data':值}}
    redis_conn.delete('remember_data')
    redis_conn.delete('none_remember_data')
    return JsonResponse({'message': 'ok'}, status=status.HTTP_200_OK)


# GET /detail/
def Detail(request):
    """房源详细信息查看"""

    # 房源名称获取
    house_id = request.GET.get('id')
    # 房源数据获取————按house_id获取
    house_infos = HouseInfo.objects.get(house_id=house_id)
    # model_to_dict()  # QuerySet类型查询数据集转换字典类型
    # print(house_infos.listing_time)

    # 获得当前时间
    now = datetime.datetime.now()
    # 转换为指定的格式:
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'detail.html', {
        "house": house_infos,  # 查询到的数据
        "now_time": otherStyleTime,  # 当前时间
    })


# 发邮件
#  GET /emailto/
def EmailToAgent(request):
    """给中介发邮件"""
    # 用户ID获取
    user_id = request.GET.get('id')
    if user_id != 'null':
        user_address = Address.objects.filter(user_id=user_id).filter(is_deleted=False)  # False为没有逻辑删除地址
        # 联系地址不为空
        if user_address:
            # print(user_address.values())
            first_address = user_address.first()  # 取第一个地址
            receiver = first_address.receiver  # 联系人
            place = first_address.place  # 地址
            mobile = first_address.mobile  # 联系方式

            # print(mobile)
            # 发邮件
            send_to_agent.delay(receiver, place, mobile)
            print('发送成功')
            return JsonResponse({'message': 'ok'}, status=status.HTTP_200_OK)
        else:
            # print(1)
            return JsonResponse({'error': '通讯地址为空，请添加后联系!'},status=status.HTTP_401_UNAUTHORIZED)
    else:
        # print(1)
        return JsonResponse({'error': '请登录'}, status=status.HTTP_400_BAD_REQUEST)
