from django.db import models

# Create your models here.
from user.models import User


class Mutual(models.Model):
    content = models.CharField('内容', max_length=100, default='')
    image_one = models.ImageField('第一张图片', default='',upload_to='one')
    image_two = models.ImageField('第二张图片', default='',upload_to='two')
    image_three = models.ImageField('第三张图片', default='',upload_to='three')
    image_four = models.ImageField('第四张图片', default='',upload_to='four')
    image_five = models.ImageField('第五张图片', default='',upload_to='five')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    # 更改时间最后删掉，不做更改朋友圈的内容的功能
    # updated_time = models.DateTimeField('修改时间', auto_now=True)
    is_delete = models.BooleanField('是否删除', default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Collection(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    mutual= models.ForeignKey(Mutual, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField('内容', max_length=50)
    parent_id = models.IntegerField('哪个评论的回复', default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    mutual = models.ForeignKey(Mutual, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)