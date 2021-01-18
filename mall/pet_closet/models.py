from django.db import models

# Create your models here.
from user.models import User


class PetCloset(models.Model):
    cloth_name=models.CharField('衣服名称',max_length=30)
    avatar = models.ImageField(upload_to='衣服图片', null=False)
    season=models.CharField('适用季节',max_length=20)
    style=models.CharField('款式',max_length=30)
    function=models.CharField('功能',max_length=30)
    remark=models.TextField('备注')
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)
    user_profile=models.ForeignKey(User,on_delete=models.CASCADE)