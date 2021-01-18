import base64
import json

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from blog.models import Mutual
from tooks.login_dec import login_check
from blog.models import Collection
from blog.models import Comment

from django.db.models import *

# Create your views here.

# 发表数据
from user.models import User
from tooks.login_dec import login_check


@login_check
def release(request, number):
    # 提交方式验证
    if request.method != 'POST':
        result = {'code': 10201, 'error': '提交方式不是post'}
        return JsonResponse(result)
    # 从token中获取用户信息,从装饰器中来
    user = request.myuser
    # 获取所有数据
    if number == 1:
        # 有文本信息也有图片
        content = request.POST.get('content')
        file_list1 = request.FILES.get('0')
        file_list2 = request.FILES.get('1')
        file_list3 = request.FILES.get('2')
        file_list4 = request.FILES.get('3')
        file_list5 = request.FILES.get('4')
        # print(1, content, type(content))
        # print(1, file_list1, type(file_list1))
        # print(1, file_list2, type(file_list2))
        # print(1, file_list3, type(file_list3))
        # print(1, file_list4, type(file_list4))
        # print(1, file_list5, type(file_list5))
        # 写入数据库
        list1 = []
        if file_list1:
            list1.append(0)
        if file_list2:
            list1.append(1)
        if file_list3:
            list1.append(2)
        if file_list4:
            list1.append(3)
        if file_list5:
            list1.append(5)
        # print(list1, len(list1))
        if len(list1) == 1:
            Mutual.objects.create(content=content,
                                  image_one=file_list1,
                                  user=user)
        elif len(list1) == 2:
            Mutual.objects.create(content=content,
                                  image_one=file_list1,
                                  image_two=file_list2,
                                  user=user)
        elif len(list1) == 3:
            Mutual.objects.create(content=content,
                                  image_one=file_list1,
                                  image_two=file_list2,
                                  image_three=file_list3,
                                  user=user)
        elif len(list1) == 4:
            Mutual.objects.create(content=content,
                                  image_one=file_list1,
                                  image_two=file_list2,
                                  image_three=file_list3,
                                  image_four=file_list4,
                                  user=user)
        elif len(list1) == 5:
            Mutual.objects.create(content=content,
                                  image_one=file_list1,
                                  image_two=file_list2,
                                  image_three=file_list3,
                                  image_four=file_list4,
                                  image_five=file_list5,
                                  user=user)

    elif number == 2:
        # 只有文本信息
        content = request.POST.get('content')
        # print(2, content, type(content))
        # 写入数据库
        Mutual.objects.create(content=content,
                              user=user)

    elif number == 3:
        # 只有图片
        file_list1 = request.FILES.get('0')
        file_list2 = request.FILES.get('1')
        file_list3 = request.FILES.get('2')
        file_list4 = request.FILES.get('3')
        file_list5 = request.FILES.get('4')
        # print(3, file_list1, type(file_list1))
        # print(3, file_list2, type(file_list2))
        # print(3, file_list3, type(file_list3))
        # print(3, file_list4, type(file_list4))
        # print(3, file_list5, type(file_list5))
        # 写入数据库
        list1 = []
        if file_list1:
            list1.append(0)
        if file_list2:
            list1.append(1)
        if file_list3:
            list1.append(2)
        if file_list4:
            list1.append(3)
        if file_list5:
            list1.append(4)
        # print(list1,len(list1))
        if len(list1) == 1:
            Mutual.objects.create(image_one=file_list1,
                                  user=user)
        elif len(list1) == 2:
            Mutual.objects.create(image_one=file_list1,
                                  image_two=file_list2,
                                  user=user)
        elif len(list1) == 3:
            Mutual.objects.create(image_one=file_list1,
                                  image_two=file_list2,
                                  image_three=file_list3,
                                  user=user)
        elif len(list1) == 4:
            Mutual.objects.create(image_one=file_list1,
                                  image_two=file_list2,
                                  image_three=file_list3,
                                  image_four=file_list4,
                                  user=user)
        elif len(list1) == 5:
            Mutual.objects.create(image_one=file_list1,
                                  image_two=file_list2,
                                  image_three=file_list3,
                                  image_four=file_list4,
                                  image_five=file_list5,
                                  user=user)
    cache.delete("listall")
    return JsonResponse({'code': 200, 'username': user.username})


# 获取列表
@login_check
def get_listall(request):
    # 提交方式验证
    if request.method != 'GET':
        result = {'code': 10204, 'error': '提交方式不是get'}
        return JsonResponse(result)
    # 从token中获取用户信息,从装饰器中来
    # user = request.myuser

    # 从数据库中获取数据之前先从缓存中查看啊，有就从缓存中获取返回，没有在到数据库中获取返回
    result = cache.get("listall")
    if result:
        print("---in cache---")
        return JsonResponse(result)

    # 从数据库mutual表中获取数据，发送到前端
    mutuals = Mutual.objects.filter(is_delete=1).order_by('created_time')
    if not mutuals:
        result = {'code': 10205, 'error': '数据库中还没有数据'}
        return JsonResponse(result)

    result = {'code': 200, 'data': []}
    # 后续还要添加点赞量和评论量2个键值
    list1 = []
    # 处理获取的数据，形成格式返回给前端
    for mutual in mutuals:
        dict1 = {}
        dict1['blog_id'] = mutual.id
        if mutual.content:
            dict1['blog_content'] = mutual.content
        if str(mutual.image_one):
            dict1['blog_image_one'] = str(mutual.image_one)
        if str(mutual.image_two):
            dict1['blog_image_two'] = str(mutual.image_two)
        if str(mutual.image_three):
            dict1['blog_image_three'] = str(mutual.image_three)
        if str(mutual.image_four):
            dict1['blog_image_four'] = str(mutual.image_four)
        if str(mutual.image_five):
            dict1['blog_image_five'] = str(mutual.image_five)
        dict1['blog_created_time'] = mutual.created_time.strftime('%Y-%m-%d %H:%M:%S')
        dict1['blog_user'] = mutual.user.username

        # 根据mutual.id进行分类获取收藏数量
        collection_set = Collection.objects.filter(mutual_id=mutual.id)
        # print(collection_set,len(collection_set))
        dict1['collection_num'] = len(collection_set)

        # 取出来数据进行处理成格式发送到前端
        comment_set = Comment.objects.filter(mutual_id=mutual.id).order_by('created_time')
        # print(comment_set, len(comment_set))
        dict1['comment_num'] = len(comment_set)

        if len(comment_set) != 0:
            msg_list = []
            for msg in comment_set:
                if msg.parent_id:
                    for msg1 in comment_set:
                        if msg1.id == msg.parent_id:
                            to_name = msg1.user.username
                            msg_list.append({
                                'id': msg.id,
                                'content': msg.content,
                                'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'self_name': msg.user.username,
                                'to_name': to_name,
                            })

                else:
                    msg_list.append({
                        'id': msg.id,
                        'content': msg.content,
                        'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'self_name': msg.user.username,
                    })

            dict1['comment'] = msg_list
            # print(msg_list)
            # for m in msg_list:
            #     print(m)

        list1.append(dict1)
        # print(dict1)
    result['data'] = list1
    # print(result)

    # 返回数据库的数据之前先在缓存中保存
    cache.set('listall', result, 60)
    return JsonResponse(result)


@login_check
def get_listuser(request, username):
    # 提交方式验证
    if request.method != 'GET':
        result = {'code': 10204, 'error': '提交方式不是get'}
        return JsonResponse(result)
    # 从token中获取用户信息,从装饰器中来
    user = request.myuser
    # 从数据库mutual表中获取数据，发送到前端

    mutuals = Mutual.objects.filter(is_delete=1, user=user).order_by('created_time')
    if not mutuals:
        result = {'code': 10205, 'error': '数据库中还没有数据'}
        return JsonResponse(result)
    # 后续还要添加点赞量和评论量2个键值
    list1 = []
    # 处理获取的数据，形成格式返回给前端
    for mutual in mutuals:
        dict1 = {}
        dict1['id'] = mutual.id
        if mutual.content:
            dict1['content'] = mutual.content
        if str(mutual.image_one):
            dict1['image_one'] = str(mutual.image_one)
        if str(mutual.image_two):
            dict1['image_two'] = str(mutual.image_two)
        if str(mutual.image_three):
            dict1['image_three'] = str(mutual.image_three)
        if str(mutual.image_four):
            dict1['image_four'] = str(mutual.image_four)
        if str(mutual.image_five):
            dict1['image_five'] = str(mutual.image_five)
        dict1['created_time'] = mutual.created_time.strftime('%Y-%m-%d %H:%M:%S')
        dict1['user'] = mutual.user.username

        # 根据mutual.id进行分类获取收藏数量
        collection_set = Collection.objects.filter(mutual_id=mutual.id)
        print(collection_set, len(collection_set))

        comment_set = Comment.objects.filter(mutual_id=mutual.id, parent_id=0)
        print(comment_set, len(comment_set))

        # 评论收藏数量需要单独获取
        dict1['comment_num'] = len(comment_set)
        dict1['collection_num'] = len(collection_set)
        list1.append(dict1)
        # print(dict1)
    print(list1)
    result = {'code': 200, 'data': list1}
    return JsonResponse(result)


@login_check
def delete_b_id(request, b_id):
    # 提交方式验证
    if request.method != 'DELETE':
        result = {'code': 10206, 'error': '提交方式不是delete'}
        return JsonResponse(result)
    # 从token中获取用户信息,从装饰器中来
    user = request.myuser
    # 从数据库mutual表中获取数据，发送到前端

    try:
        mutual = Mutual.objects.get(is_delete=1, user=user, id=b_id)
    except:
        result = {'code': 10207, 'error': 'b_id 不正确'}
        return JsonResponse(result)
    mutual.is_delete = 0
    mutual.save()
    cache.delete("listall")
    return JsonResponse({'code': 200, 'data': '删除成功'})


@login_check
def collection_username_b_id(request, username, b_id):
    # 对用户姓名和发表信息的id先做判断，看存在不
    # 根据2个值吧数据写入数据库
    print(username, b_id)

    # 从token中获取用户信息,从装饰器中来
    # user = request.myuser
    # 从数据库mutual表中获取数据，发送到前端

    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'code': 10209, 'data': '该用户不在数据库中'})
    print(user.username, user.id)

    res = Collection.objects.filter(mutual_id=b_id, user_id=user.id)
    print(res)
    if not res:
        Collection.objects.create(mutual_id=b_id, user=user)
        return JsonResponse({'code': 200, 'data': '收藏成功'})
    result = {'code': 10208, 'error': '该b_id您已经收藏过了'}
    cache.delete("listall")
    return JsonResponse(result)


@login_check
def comment_username_b_id(request, username, b_id):
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'code': 10210, 'data': '该用户不在数据库中'})

    json_str = request.body
    py_obj = json.loads(json_str)
    comment = py_obj['comment']
    print(username, b_id, comment)

    # 数据中写入评论的数据
    Comment.objects.create(content=comment, parent_id=0, mutual_id=b_id, user=user)
    cache.delete("listall")
    return JsonResponse({'code': 200, 'data': '评论成功'})


@login_check
def restore_username_b_id_c_id(request, username, b_id, c_id):
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'code': 10211, 'data': '该用户不在数据库中'})

    json_str = request.body
    py_obj = json.loads(json_str)
    restore = py_obj['restore']
    print(username, b_id, c_id, restore)

    # 数据中写入评论的数据
    Comment.objects.create(content=restore, parent_id=c_id, mutual_id=b_id, user=user)
    cache.delete("listall")
    return JsonResponse({'code': 200, 'data': '回复成功'})
