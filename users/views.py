#encoding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
import json
from json import JSONDecodeError

from users.models import Users
from users.api_wechat import get_openid
from users.jwt_token import create_token, verify_token

# Create your views here.

def login(request):
    pass
    return JsonResponse({'data': 1})

def login_wechat(request):
    # 验证请求的方法
    if request.method != "POST":
        return JsonResponse({'ret': False, 'error_code': 1})

    # 验证请求的主题是否可以被转换成json格式
    try:
        print("body is ", request.body)
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'ret': False, 'error_code': 2})

    # 读取请求的参数
    try:
        code = data['code']
        name = data['name']
        avatarUrl = data['avatarUrl']
    except KeyError:
        return JsonResponse({'ret': False, 'error_code': 3})

    # 验证openid
    open_id = get_openid(code)
    if not open_id:
        return JsonResponse({'ret': False, 'error_code': 4})

    # 尝试从User中获取该对象，如果不存在，则新建该对象
    try:
        user = Users.objects.get(open_id=open_id)
    except Users.DoesNotExist:
        user = Users.objects.create(account=name, open_id=open_id)
    user.avatarUrl = avatarUrl
    user.save()

    token = create_token(user.id)
    return JsonResponse({'ret': True, 'ID': str(user.id), 'Token': token})

def get_my_profile(request):
    if request.method != "GET":
        return JsonResponse({"ret": False, 'error_code': 1})
    
    user = verify_token(request.META.get('HTTP_AUTHORIZATION'))
    if not user:
        return JsonResponse({"ret": False, 'error_code': 5})

    return JsonResponse(
        {
            'ret': True,
            'account': user.account,
            'name': user.name,
            'age': user.age,
            'sex': user.sex,
            'avatarUrl': user.avatarUrl
        })

def modify_my_profile(request):
    if request.method != "POST":
        return JsonResponse({'ret': False, 'error_code': 1})
    
    user = verify_token(request.META.get('HTTP_AUTHORIZATION'))
    if not user:
        return JsonResponse({'ret': False, 'error_code': 5})

    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'ret': False, 'error_code': 3})

    try:
        name = data['name']
        age = data['age']
        sex = data['sex']
    except KeyError:
        return JsonResponse({'ret': False, 'error_code': 2})

    if type(age) != int or age < 0 or age > 200:
        return JsonResponse({'ret': False, 'error_code': 3})

    user.name = name
    user.age = age
    user.sex = sex

    try:
        user.full_clean()
        user.save()
    except ValidationError:
        return JsonResponse({'ret': False, 'error_code': 3})

    return JsonResponse({'ret': True})
















