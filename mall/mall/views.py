import json
import time
import jwt
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from tooks.login_dec import login_check

def test_login(request):
    if request.method != 'POST':
        result = {'code': 10101, 'error': '提交方式不是post'}
        return JsonResponse(result)
    json_str = request.body
    py_obj = json.loads(json_str)
    username = py_obj['username']
    password = py_obj['password']
    print(username, password)

    token = login_check(username).decode()
    return JsonResponse({'code': 200, 'token': token, 'username': username})

