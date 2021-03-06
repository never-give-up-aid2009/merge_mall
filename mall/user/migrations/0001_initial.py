# Generated by Django 2.2.12 on 2021-01-16 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('avatar', models.ImageField(null='True', upload_to='', verbose_name='头像')),
                ('birthday', models.CharField(max_length=10, null='True', verbose_name='生日')),
            ],
        ),
    ]
