#encoding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ValidationError

import json
import re
import datetime
from random import randint
from json import JSONDecodeError

from users.jwt_token import verify_token
from users.models import Users

from news.models import Post
from news.models import PostLabel

from news.utils import encode_label
from news.utils import decode_label
from news.utils import check_postLabel
from news.utils import rank_post

post_title_pattern = re.compile(r"^.{1,50}$")
deadline_pattern = re.compile(r"^\d\d\d\d-\d\d-\d\d$")

def post_news(request):
    if request.method != "POST":
        return JsonResponse({'ret': False, 'error_code': 1})

    # 检查用户身份
    user = verify_token(request.META.get('HTTP_AUTHORIZATION'))
    if not user:
        return JsonResponse({'ret': False, 'error_code': 5})

    # try:
    # print(request.body)
    # print(type(request.body))
    data = json.loads(request.body)
    # except JSONDecodeError:
        # return JsonResponse({'ret': False, 'error_code': 3})

    try:
        title = data['title']
        post_detail = data['postDetail']
        deadline = data['ddl']
        labels = data['labels']
    except KeyError:
        return JsonResponse({'ret': False, 'error_code': 2})

    labelList = decode_label(labels)
    if not check_postLabel(labelList):
        print("cant check_postLabel")
        return JsonResponse({'ret': False, 'error_code': 3})

    # 检查各字段的合法性
    if not post_title_pattern.match(title):
        print("title does not match")
        return JsonResponse({'ret': False, 'error_code': 3})
    if not deadline_pattern.match(deadline):
        print("ddl does not match")
        return JsonResponse({'ret': False, 'error_code': 3})
    try:
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
    except ValueError:
        print("ddl valueError")
        return JsonResponse({'ret': False, 'error_code': 3})

    # 如果重复了 则不可以加入到项目
    if Post.objects.filter(title=title, post_detail=post_detail, deadline=deadline, poster=user).exists():
        return JsonResponse({'ret': False, 'error_code': 4})

    new_post = Post.objects.create(
        title = title,
        post_detail = post_detail,
        deadline = deadline,
        poster = user,
        image='img/post/example/' + str(randint(1,4)) + '.jpg',
        is_imported = False,
    )

    for i in labelList:
        new_post.postlabel_set.create(label=i)
    return JsonResponse({'ret': True, 'postID': str(new_post.id)})


def get_unclosed_posts(request):
    if request.method != "POST":
        return JsonResponse({'ret': False, 'error_code': 1})

    user = verify_token(request.META.get('HTTP_AUTHORIZATION'))
    if not user:
        return JsonResponse({'ret': False, 'error_code': 5})

    # 获取用户的历史纪录
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'ret': False, 'error_code': 3})
    try:
        history = data['history']
        history = decode_label(history)
    except KeyError:
        return JsonResponse({'ret': False, 'error_code': 2})

    label_weight = {}
    weight_base = 1
    # 分析历史纪录
    for post_id in history:
        post_label = PostLabel.objects.filter(post_id=post_id).all()
        for label in post_label:
            if label.label in label_weight:
                label_weight[label.label] += weight_base
            else:
                label_weight[label.label] = weight_base
        weight_base += 1

    unclosed_posts = Post.objects.filter(if_end=False, deadline__gte=datetime.date.today()).order_by('-post_time')
    ret_data = []
    for post in unclosed_posts:
        # 整理相应项目的标签
        post_weight = 0
        label_list = PostLabel.objects.filter(post=post).all()
        for label in label_list:
            if label.label in label_weight:
                post_weight += label_weight[label.label]
        labels = encode_label(label_list)

        ret_data.append({
            "title": post.title,
            "postDetail": post.post_detail,
            "ddl": post.deadline,
            "postID": str(post.id),
            "posterID": str(post.poster.id),
            "poster_name": post.poster.name,
            "poster_avatar_url": post.poster.avatarUrl,
            "image_url": post.image.url,
            "labels": labels,
            "is_imported": post.is_imported,
            "weight": post_weight,
        })

    # 根据推荐算法对返回的Post进行排序
    ret_data = rank_post(ret_data)

    return JsonResponse(ret_data, safe=False)

def upload_post_image(request, post_id):
    if request.method != "POST":
        return JsonResponse({'ret': False, 'error_code': 1})

    user = verify_token(request.META.get('HTTP_AUTHORIZATION'))
    if not user:
        return JsonResponse({'ret': False, 'error_code': 5})

    if request.content_type != 'multipart/form-data':
        return JsonResponse({'ret': False, 'error_code': 3})
    image = request.FILES.get('image')
    if not image:
        return JsonResponse({'ret': False, 'error_code': 2})

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'ret': False, 'error_code': 4})
    if post.poster != user:
        return JsonResponse({'ret': False, 'error_code': 6})


    print("post image: ", post.image)
    try:
        post.image = image
        # post.if_end = False
        post.full_clean()  # 检查格式
        post.save()
    except ValidationError:
        return JsonResponse({'ret': False, 'error_code': 3})

    print("post image: ", post.image)
    return JsonResponse({'ret': True, 'image_url': post.image.url})

def get_news(request):
    return JsonResponse({'ret': False})


 
 

