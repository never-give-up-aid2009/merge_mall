import hashlib
import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from user.models import User

# Create your views here.
from user.views import make_token


class Tokenviews(View):
    # 如果是get请求
    def get(self,request):
        return HttpResponse('get tokens')
    # 如果是post请求
    def post(self,request):
        # 获取前端发送的json对象
        json_str = request.body
        # 反序列化json对象
        py_obj = json.loads(json_str)
        # 从前端页面获取需要的键和值
        username = py_obj['username']
        pwd = py_obj['pwd']
        print(username,pwd)
        # 校验用户名和密码
        try:
            user = User.objects.get(username=username)
        except:
            result = {'code':20000,'error':'用户名或密码错误'}
            return JsonResponse(result)
        # 将获取到的用户输入密码进行加密
        md5 = hashlib.md5()
        # decode的作用是将二进制数据解码成unicode编码,是给人看
        # encode的作用是将unicode编码的字符串编码成二进制数据，是给计算机看
        md5.update(pwd.encode())
        # 生成十六进制加密编码
        pwd_h =md5.hexdigest()
        # 将用户输入的密码与我们数据库中的进行比对
        if pwd_h != user.password:
            result = {'code':20000,'error':'用户名或者密码错误'}
            return JsonResponse(result)
        # 签发token
        token = make_token(username)
        return JsonResponse({'code':200,'username':username,
                             'data':{'token':token.decode()}})