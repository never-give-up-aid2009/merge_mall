from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
import os
import time

from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from pet_closet.models import PetCloset
from tooks.login_dec import login_check
from user.models import User

import json
import time
import requests
import re
from fake_useragent import UserAgent


# @login_check
def add_view(request):
    if request.method == "POST":
        # user_profile=request.myuser
        # print(user_profile)

        cloth_name = request.POST.get('cloth_name')
        avatar = request.FILES.get('avatar')
        season = request.POST.get('season')
        style = request.POST.get('style')
        function = request.POST.get('function')
        remark = request.POST.get('remark')
        print(cloth_name,season,style,function,remark)
        # user = request.myuser
        user_profile = request.POST.get('cloth_name')
        # print(user_profile)
        try:
            # user = UserProfile.objects.create(username='bzx', email='1333', phone='13131',
            #                       password='1313', nickname='bzx1')
            pet_closet = PetCloset.objects.create(cloth_name=cloth_name, avatar=avatar, season=season,
                                                  style=style, function=function, remark=remark,
                                                  user_profile_id='王午阳')
        except Exception as e:
            print(e)
            result = {'code': 10103, 'error': '用户名已经存在'}
            return JsonResponse(result)
        result = {"code": 200, "msg": "上传照片成功"}
        return JsonResponse(result)


class Weather:
    # ---------根据主机IP获取定位-----
    def search_region_by_ip(self, computer_ip):
        url = 'https://www.ip138.com/iplookup.asp?ip=%s&action=2' % computer_ip
        headers = {'User-Agent': UserAgent().random}
        try:
            html = requests.get(url=url, headers=headers).content.decode('gb2312')
            # print(html)
            region = re.findall('ip_result = {"ASN归属地":".*?[省市](.*?)市[\W|\w]', html, re.S)
            return region
        except Exception:
            return JsonResponse({'code': 50001, 'error': '查询region失败'})

    def search_weather(self, region):
        url = "http://wthrcdn.etouch.cn/weather_mini?city=%s" % region
        try:
            # response = requests.get(url,timeout=8)
            response = requests.get(url)
            weather_data = json.loads(response.text)
            # print(weather_data)
            date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            year = str(date).split("-")[0]
            month = str(date).split("-")[1]
            day = weather_data['data']['forecast'][0]['date']
            city = weather_data['data']['city']
            weather_high = weather_data['data']['forecast'][0]['high']
            weather_low = weather_data['data']['forecast'][0]['low']
            a = weather_low.split(" ")[1]
            # print(a)
            print(year, month, day, weather_high, weather_low)
            region_weather = (year + '/' + month + '/' + day + '  ' + weather_high + '  ' + weather_low)
            return region_weather
        except:
            return JsonResponse({'code': 50002, 'error': '查询weather失败'})


def weather_view(request, bzx):
    url = 'http://ip.42.pl/raw'
    computer_ip = requests.get(url).text
    # print(computer_ip)
    weather = Weather()
    region = weather.search_region_by_ip(computer_ip)[0]
    # print(region)
    # region = '北京'
    region_weather = weather.search_weather(region)
    # result = {'code':200,}
    # result = {'code': 200, 'data': {'info': '123'}}
    # return JsonResponse(result)
    return JsonResponse({'code': 200, 'data': {'region': region, 'weather': region_weather}})

# @login_check
def list_view(request):
    if request.method == 'GET':
        all_clothes = PetCloset.objects.all().order_by('-created_time')
        count = len(all_clothes)
        clothes_json = []
        for i in all_clothes:
            clothes_json2 = {}
            clothes_json2['id'] = i.id
            clothes_json2['cloth_name'] = i.cloth_name
            # clothes_json2['avatar'] = i.avatar
            clothes_json2['season'] = i.season
            clothes_json2['style'] = i.style
            clothes_json2['function'] = i.function
            clothes_json2['remark'] = i.remark
            clothes_json2['created_time'] = i.created_time
            clothes_json2['updated_time'] = i.updated_time
            clothes_json.append(clothes_json2)
        return JsonResponse({"code": 200, "obj": clothes_json})
    elif request.method == "POST":
        clothes_json = []
        json_str = request.body
        json_obj = json.loads(json_str)
        cloth_name = json_obj['name']
        print(cloth_name)
        clothes = PetCloset.objects.filter(cloth_name=cloth_name)
        if clothes:
            clothes_json2 = {}
            clothes_json2['id'] = clothes[0].id
            clothes_json2['cloth_name'] = clothes[0].cloth_name
            # clothes_json2['avatar'] =  clothes.avatar
            clothes_json2['season'] = clothes[0].season
            clothes_json2['style'] = clothes[0].style
            clothes_json2['function'] = clothes[0].function
            clothes_json2['remark'] = clothes[0].remark
            clothes_json2['created_time'] = clothes[0].created_time
            clothes_json2['updated_time'] = clothes[0].updated_time
            clothes_json.append(clothes_json2)
            print(clothes_json)
            return JsonResponse({"code": 200, "obj": clothes_json})

        else:
            return JsonResponse({'code': 50003, 'error': '查询关键字失败'})

# @login_check
def del_view(request):
    if request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        id = json_obj["id"]
        try:
            notice = PetCloset.objects.get(id=id)
            notice.delete()
        except Exception as e:
            print(e)
            return JsonResponse({"code": 300})
        return JsonResponse({"code": 200})

# @login_check
def update_view(request):
    if request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        id = json_obj["id"]
        # print(id)
        clothes_json = {}
        try:
            cloth = PetCloset.objects.get(id=id)
            clothes_json = {}
            clothes_json['id'] = cloth.id
            clothes_json['cloth_name'] = cloth.cloth_name
            # clothes_json2['avatar'] =  cloth.avatar
            clothes_json['season'] = cloth.season
            clothes_json['style'] = cloth.style
            clothes_json['function'] = cloth.function
            clothes_json['remark'] = cloth.remark
            # print(clothes_json)
        except Exception as e:
            return JsonResponse({"code": 50004, 'error': '查找不到'})
        return JsonResponse({"code": 200, "obj": clothes_json})

# @login_check
def update1_view(request):
    if request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        id = json_obj["uid"]
        cloth_name = json_obj["cloth_name"]
        season = json_obj["season"]
        style = json_obj["style"]
        function1 = json_obj["function1"]
        remark = json_obj["remark"]
        print(id)
        print(cloth_name)
        print(season)
        print(style)
        print(function1)
        print(remark)
        try:
            tar_cloth = PetCloset.objects.get(id=id)
            tar_cloth.cloth_name = json_obj["cloth_name"]
            tar_cloth.season = json_obj["season"]
            tar_cloth.style = json_obj["style"]
            tar_cloth.function1 = json_obj["function1"]
            tar_cloth.remark = json_obj["remark"]
            tar_cloth.save()
            print(tar_cloth)
        except Exception as e:
            return JsonResponse({"code": 50005, 'error': '查找不到'})
        return JsonResponse({"code": 200})

