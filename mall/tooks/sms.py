import datetime
import hashlib
import base64
import json
import requests  # 使用该库可以发送http/https请求


class YunTongXin():
    base_url = 'https://app.cloopen.com:8883'

    def __init__(self, accountSid, accountToken, appId, templateId):
        # 定义我们所需要的参数
        self.accountSid = accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId

    # 1 生成url：baseurl+业务url
    def get_request_url(self, sig):
        self.url = self.base_url + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % (self.accountSid, sig)
        return self.url

    # 2 生成时间戳
    def get_timestamp(self):
        # 获取当前时间
        now = datetime.datetime.now()
        # 将获取的当前时间转换为字符串，要年月份时分秒格式
        now_str = now.strftime("%Y%m%d%H%M%S")
        # 返回格式化的时间戳供后边用
        return now_str

    # 生成SigParameter: MD5加密（账户Id + 账户授权令牌 + 时间戳）,转大写
    def get_sig(self, timestamp):# timestamp就是生成的时间戳
        s = self.accountSid + self.accountToken + timestamp
        md5 = hashlib.md5()
        md5.update(s.encode())
        return md5.hexdigest().upper()# 生成十六进制的编码并且转为大写

    # 2 构造请求包的包头
    def get_request_header(self, timestamp):
        # 按照云联云要求的固定格式
        # Authorization: Base64编码（账户Id + 冒号 + 时间戳）
        s = self.accountSid + ':' + timestamp
        # 传参时要转为encode，结果要是decode的
        b_s = base64.b64encode(s.encode()).decode()
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            # Authorization:Base64编码（账户Id + 冒号 + 时间戳）
            'Authorization': b_s
        }

    # 3 构造请求包的包体
    def get_request_body(self, phone, code):
        data = {
            'to': phone,
            'appId': self.appId,
            'templateId': self.templateId,
            'datas': [code, '3']
        }
        return data

    # 4 发送请求的方法
    def do_request(self, url, header, body):
        # 前边的data为字典，用json前必须转为字符串
        res = requests.post(url, headers=header,data=json.dumps(body))
        # 返回响应的文本
        return res.text

    # 将以上步骤封装到一起
    def run(self, phone, code):
        # 1 构造url
        timestamp = self.get_timestamp()
        sig = self.get_sig(timestamp)
        url = self.get_request_url(sig)
        print(url)
        # 2 header
        header = self.get_request_header(timestamp)
        print(header)
        # 3 body
        body = self.get_request_body(phone, code)
        print(body)
        # 4 发送请求
        res = self.do_request(url, header, body)
        return res


# if __name__ == '__main__':
#     # 输入你自己主机在云联云上获得的数据
#     aid = '8aaf0708762cb1cf0176b3105383313d'
#     token = 'c7ceb02d91804ccab7ea2791f34766a4'
#     appid = '8aaf0708762cb1cf0176b31053fc3143'
#     tid = '1'
#     x = YunTongXin(aid, token, appid, tid)
#     res = x.run('13649232510', '123456')
#     print(res)
