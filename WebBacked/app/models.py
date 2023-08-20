# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from mdeditor.fields import MDTextField
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import User


'''
User 模型：用于存储用户信息，包括用户名和密码等。

Role 模型：用于定义角色，每个角色可以有不同的权限。

Permission 模型：用于定义权限，每个权限对应某个具体操作或功能。

UserRole 模型：建立用户和角色之间的关联关系，表示某个用户拥有哪些角色。

RolePermission 模型：建立角色和权限之间的关联关系，表示某个角色具有哪些权限。'''

class User(models.Model):
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255) 
     
    class Meta:
        # managed = False
        verbose_name_plural = '用户列表'
    def __str__(self):
        return self.username


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        # managed = False
        verbose_name_plural = '角色列表'

class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        # managed = False
        verbose_name_plural = '权限列表'

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    class Meta:
        # managed = False
        verbose_name_plural = '用户角色列表'

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    class Meta:
        # managed = False
        verbose_name_plural = '角色权限列表'








# class User(AbstractUser):

#     """用户模型类
#     创建自定义的用户模型类
#     Django认证系统中提供的用户模型类及方法很方便，我们可以使用这个模型类，但是字段有些无法满足项目需求，如本项目中需要保存用户的手机号，
#     需要给模型类添加额外的字段。
#     Django提供了django.contrib.auth.models.AbstractUser用户抽象模型类允许我们继承，扩展字段来使用Django认证系统的用户模型类。
#     我们自定义的用户模型类还不能直接被Django的认证系统所识别，需要在配置文件中告知Django认证系统使用我们自定义的模型类。
#     在配置文件中进行设置
#     AUTH_USER_MODEL = 'users.User'
#     AUTH_USER_MODEL 参数的设置以点.来分隔，表示应用名.模型类名。
#     """
#     mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
 
#     class Meta:
#         db_table = 'tb_users'
#         verbose_name = '用户'
#         verbose_name_plural = verbose_name




class ImageTable(models.Model):
    url = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    source = models.BinaryField(blank=True, null=True)
    is_public = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'image_table'
        verbose_name_plural = '图片列表'


class NovelTable(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    des = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    is_public = models.IntegerField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'novel_table'
        verbose_name_plural = '小说列表'


'''博客文章'''
class BlogPost(models.Model):

    url = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='文章标题', unique = True)
    category = models.CharField(max_length=50, blank=True, null=True)
    isTop=models.BooleanField(default=False,verbose_name='是否置顶')
    isHot=models.BooleanField(default=False,verbose_name='是否热门')
    des=models.CharField(max_length=500,verbose_name='内容摘要',default='')
    content=MDTextField(verbose_name='内容')
    viewsCount= models.IntegerField(default=0, verbose_name="查看数")
    commentsCount=models.IntegerField(default=0, verbose_name="评论数")
    crawl_time = models.DateTimeField(default=timezone.now,blank=True, null=True)

    def __str__(self):
            return self.title

    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'
