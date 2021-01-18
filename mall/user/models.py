from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField('用户名',max_length=30,primary_key=True)
    password = models.CharField('密码',max_length=32)
    email = models.EmailField('邮箱')
    phone = models.CharField('手机号',max_length=11)
    avatar = models.ImageField('头像',null='True')
    birthday = models.CharField('生日',max_length=10,null='True')
