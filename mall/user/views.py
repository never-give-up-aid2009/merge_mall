import hashlib
import json
import random
import time
import jwt
import redis

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
# Create your views here.
from mall import settings
# from tools.login_dec import login_check
from tooks.login_dec import login_check
from tooks.sms import YunTongXin
from user.models import User



class UserViews(View):
    # 后端接收到前端的get请求
    def get(self,requset):
        return HttpResponse('user get')
    # 后端接收前端的post请求
    def post(self,request):
        # 获取前端发送的json对象
        json_str = request.body
        # 反序列化
        py_obj = json.loads(json_str)
        # 根据键获取值
        username= py_obj['username']
        pwd = py_obj['pwd']
        cpwd = py_obj['cpwd']
        email = py_obj['email']
        phone = py_obj['phone']
        sms_num = py_obj['sms_num']
        # 1 检查用户名长度
        if len(username)>30:
            result = {'code':10005,'error':'用户名长度超出30！'}
            return JsonResponse(result)
        # 2 检查两次密码是否一致
        if pwd != cpwd:
            result = {'code':10000,'error':'两次密码输入要一致！'}
            return JsonResponse(result)
        # 3 检查手机号码格式是否正确
        if len(phone) != 11:
            result = {'code':10004,'error':'手机号错误！'}
            return JsonResponse(result)
        # 4 检查email
        if not email:
            result = {"code": 10003, "error": "邮箱错误！"}
            return JsonResponse(result)
        #5 用户名是否可用
        c_user = User.objects.filter(username = username)
        if c_user:
            result = {"code": 10001, "error": "用户名已被占用！"}
            return JsonResponse(result)
        # 6 密码加密
        md5 = hashlib.md5()
        #转换为二进制码
        md5.update(pwd.encode())
        pwd_h = md5.hexdigest()
        # 7 验证手机验证码
          # 7.1 获取redis中暂存的验证码
        cache_key = 'sms_%s'%phone
        cache_code = cache.get(cache_key)
          # 7.2 判断redis中的验证码是否为空
        if not cache_code:
            result = {'code':20002,'error':'验证码已过期'}
            return JsonResponse(result)
          # 7.3 用户输入的和redis中的验证码是否相等
        if int(sms_num) != cache_code:
            result = {'code': 20001, 'error': '验证码输入错误'}
            return JsonResponse(result)
        # 8 数据入库
        try:
            user = User.objects.create(username=username,
                                      password=pwd_h,
                                      email = email,
                                      phone=phone)
        except:
            result = {"code":10001,"error":"用户名已存在！"}
            return JsonResponse(result)

        #签发token
        token = make_token(username)
        return JsonResponse({"code":200,"username":username,
                             "data":{"token":token.decode()}})

    @method_decorator(login_check)
    def put(self, request, username):

        json_str = request.body
        py_obj = json.loads(json_str)
        sign = py_obj['sign']
        nickname = py_obj['nickname']
        info = py_obj['info']
        print(sign, nickname, info)

        user = request.myuser
        user.sign = sign
        user.nickname = nickname
        user.info = info
        user.save()

        result = {'code': 200, 'username': user.username}
        return JsonResponse(result)

def make_token(username, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {"username": username, "exp": now + expire}
    return jwt.encode(payload, key, algorithm="HS256")


def sms_view(request):
    # 获取前端发送的数据
    json_str = request.body
    # 将获取到的json数据反序列化
    py_obj = json.loads(json_str)
    # 获取我们所需要的值
    phone = py_obj['phone']
    code = random.randint(1000,9999)
    print(phone,code)
    # 先将验证码暂存在redis中，用来在注册时使用
    cache_key = 'sms_%s'%phone
    # 存入
    cache.set(cache_key,code,120)
    # 异步方式发送（将发送短信的任务放到队列中，立即返回）
    # send_sms.delay(phone,code)


    # 发送短信验证码
    x = YunTongXin(settings.SMS_ACCOUNT_ID,
                   settings.SMS_ACCOUNT_TOKEN,
                   settings.SMS_APP_ID,
                   settings.SMS_TEMPLATE_ID)
    res = x.run(phone,code)
    # print(res)
    # res1 = json.loads(res)

    return JsonResponse({'code':200})
    # print(phone,code)

