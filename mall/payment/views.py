import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from tooks.login_dec import login_check
# Create your views here.
from django.views import View
from alipay import AliPay
from django.conf import settings
from product.models import Product


def get_order(request,p_id):
     if request.method == 'POST':
            result = {'code': 10204, 'error': '提交方式不是post'}
            return JsonResponse(result)
        #从数据库Product表中获取数据，发送到前端
     elif request.method == 'GET':
         print('p_id',p_id)
         product = Product.objects.filter(id=p_id)
         # print(product[0].kind)
         # print(product[0].id)
         if not product:
                result = {'code': 10401, 'error': '数据库没有这个商品'}
                return JsonResponse(result)
            # 处理获取的数据，形成格式返回给前端
         dict3 = {}
         dict3['id'] = product[0].id
         dict3['name']= product[0].kind
         dict3['price'] = product[0].price
         # dict3['count'] = product.count
         print(dict3)
         result = {'code': 200, 'data': dict3}
         # result = {'code': 200, 'name': 'uuuuu'}
         return JsonResponse(result)


app_private_key_string = open(settings.ALIPAY_KEY_DIR+'app_private_key.pem').read()
alipay_public_key_string=open(settings.ALIPAY_KEY_DIR+'alipay_public_key.pem').read()

#订单状态  1:未支付   2：支付成功   3：支付失败
ORDER_STATUS = 1

class MyAliPay(View):
    #初始化与支付相关的参数
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.alipay=AliPay(
            # 应用id
            appid=settings.ALIPAY_APP_ID,
            #用于被动的接受支付结果的url
            app_notify_url=None,
            #当前app的私钥
            app_private_key_string=app_private_key_string,
            #支付宝公钥
            alipay_public_key_string=alipay_public_key_string,
            #使用的签名算法
            sign_type='RSA2',
            #指定是测试模式
            debug=True,
        )
    #2 生成pay_url的方法
    def get_trade_url(self,order_id,payall):
        base_url='https://openapi.alipaydev.com/gateway.do'
        order_string=self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=payall,
            # 订单标题
            subject=order_id,
            #用户支付完毕后，跳转的地方
            return_url=settings.ALIPAY_RETURN_URL,
            #被动的接收支付结果的url
            notify_url=settings.ALIPAY_NOTIFY_URL,
        )

        return base_url+"?"+order_string

    def get_verify_result(self, data, sign):
        return self.alipay.verify(data, sign)

    #3 获取订单状态的方法
    def get_trade_result(self,order_id):
        result = self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        if result.get('trade_status')=='TRADE_SUCCESS':
            return True
        return False


class JumpView(MyAliPay):
    def post(self,request):
        json_obj = json.loads(request.body)
        order_id=json_obj['order_id']
        payall=json_obj['payall']
        pay_url=self.get_trade_url(order_id,int(payall))
        print(order_id,payall)
        return JsonResponse({'pay_url':pay_url})


class ResultView(MyAliPay):
    def get(self, request):
        # return HttpResponse('支付成功！')
        request_data = {k: request.GET[k] for k in request.GET.keys()}
        # 从请求数据中取出订单编号
        order_id = request_data['out_trade_no']
        if ORDER_STATUS == 2:
            result = {'code': 200, 'data': '支付成功'}
            return JsonResponse(result)

        elif ORDER_STATUS == 1:
            # 意味着接收POST请求的服务器挂了，需要我们主动查询
            result = self.get_trade_result(order_id)
            if result:
                # 修改数据库的订单状态由未支付转为支付成功
                # return HttpResponse("主动查询支付成功！")
                result = {'code': 200,'data':'支付成功'}
                return JsonResponse(result)

            else:
                # 修改数据库的订单状态由未支付转为支付失败

                result = {'code':201,'data':'支付失败'}
                return JsonResponse(result)

        else:
            result = {'code': 201,'data':'请求不合法'}
            return JsonResponse(result)
            # return HttpResponse('请求不合法')

