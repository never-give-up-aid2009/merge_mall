from django.db import models
from user.models import User
from tooks.ImageStorage import ImageStorage


# Create your models here.

class Product(models.Model):
    kind = models.CharField('种类', max_length=20)
    # 两类：tec技术类 no-tec非技术类
    age = models.IntegerField('宠物年龄')
    # public公开 private私有
    sex = models.CharField('宠物性别', max_length=10)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    price = models.IntegerField('价格')
    address = models.CharField('地址', max_length=50)
    c_img = models.CharField('图片', max_length=100)
    way = models.CharField('方式', max_length=50)
    describe = models.TextField('内容')
    user_profile = models.ForeignKey(User,on_delete=models.CASCADE)


class Image(models.Model):
    c_img = models.ImageField(upload_to='c_img', storage=ImageStorage())
