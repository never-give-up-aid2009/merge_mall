from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import json

from tooks.login_dec import login_check
from .models import Product,Image
from user.models import User
from django.core.cache import cache

# from django.conf import settings

# Create your views here.

def make_products_res(products):
    product_res=[]
    for product in products:
        d={}
        d['id'] = product.id
        d['kind']=product.kind
        d['age']=product.age
        d['sex']=product.sex
        d['price']=product.price
        d['address'] = product.address
        d['c_img'] = product.c_img
        d['way'] = product.way
        d['describe'] = product.describe
        product_res.append(d)
    res={'code':200,'data':{}}
    res['data']['products']=product_res
    return res

def upload_img(request,username):
    if request.method != 'POST':
        result = {'code': 213, 'error': '请发送post请求'}
        return JsonResponse(result)
    c_img = request.FILES['c_img']
    c_img=Image.objects.create(c_img=c_img)
    print(c_img.c_img)
    result = {'code': 200,'c_img':str(c_img.c_img)}
    return JsonResponse(result)


def upload_product(request,username):
        print(username)
        if request.method !='POST':
            result = {'code': 212, 'error': '错误'}
            return JsonResponse(result)
        elif request.method=='POST':
            #获取前端提交的数据
            json_str = request.body
            py_obj = json.loads(json_str)
            kind = py_obj['kind']
            sex = py_obj['sex']
            way = py_obj['way']
            age = py_obj['age']
            price = py_obj['price']
            city = py_obj['city']
            describe = py_obj['describe']
            c_img = py_obj['c_img']
            print(kind,sex,way,age,price,city,describe,c_img)
            user = User.objects.get(username=username)  ##
            Product.objects.create(
                kind=kind, sex=sex, way=way, age=age,
                price=price, address=city, describe=describe, c_img=c_img,
                user_profile=user
            )

            result = {'code': 200,'username': username}
            return JsonResponse(result)

def product_search(request,username):
    if request.method == 'POST':
        json_str = request.body
        py_obj = json.loads(json_str)
        info = py_obj['info']
        print(info)
        cache_key = info
        cache.set('key', cache_key, 3)
        res = {'code': 200}
        return JsonResponse(res)
def product_list(request,username):
    info=cache.get('key')
    print('info',info)
    way=info.split(',')[0]
    kind=info.split(',',1)[1]
    kind_list=kind.split(',')
    products=Product.objects.filter(kind__in=kind_list,way=way)
    res = make_products_res(products)
    print(res)
    # s = request.GET.get('var1')
    # s += 'world'
    # s = {'code': 200, 's':s}
    return JsonResponse(res)
def product_detail(request,username):
    id = request.GET.get('id')
    print('id:',id)
    products = Product.objects.filter(id=id)
    res = make_products_res(products)
    print('detail:',res)
    return JsonResponse(res)