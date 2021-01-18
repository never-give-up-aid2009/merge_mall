from django.http import JsonResponse
import jwt
from django.conf import settings
from user.models import User


def login_check(func):
    def wrap(request, *args, **kwargs):
        # 从用户的请求中获取token
        token = request.META.get('HTTP_AUTHORIZATION')
        # 是否有token
        if not token:
            result = {'code': 403, 'error': '请登录'}
            return JsonResponse(result)
        # 校验token，token是否有效
        try:
            payload = jwt.decode(token, settings.JWT_TOKEN_KEY,
                                 algorithm='HS256')
        except:
            result = {'code': 403, 'error': '请登录'}
            return JsonResponse(result)
        username = payload['username']
        user = User.objects.get(username=username)
        # 将user保存到request对象的附加属性
        request.myuser = user
        return func(request, *args, **kwargs)

    return wrap


def get_user_by_request(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.JWT_TOKEN_KEY)
    except:
        return None
    username = payload['username']
    return username
