from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ImageTable, NovelTable,User,BlogPost,Role, Permission, UserRole, RolePermission

class ImageTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'crawl_time')  # 要显示的字段
    list_filter = ('category',)  # 过滤器   在右边显示
    search_fields = ('title', 'category')  # 搜索字段 表示可以根据标题和分类来搜索图片


class NovelTableAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'crawl_time')
    list_filter = ('category',)  # 过滤器   在右边显示
    search_fields = ('title', 'author', 'category')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title','isTop','isHot']

admin.site.register(ImageTable, ImageTableAdmin)
admin.site.register(NovelTable, NovelTableAdmin)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(UserRole)
admin.site.register(RolePermission)