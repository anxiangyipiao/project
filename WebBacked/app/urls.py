"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(r'images/', views.image_list, name='image_list'),
    path(r'novels/', views.novel_list, name='novel_list'),
    path(r'blogs/', views.blog_list, name='blog_list'),
    path(r'blog_detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.logout, name='logout'),
    path(r'register/', views.register, name='register'),
    path(r'captcha/', include('captcha.urls')), 
    path(r'mdeditor/', include('mdeditor.urls')),
    path(r'searchimage/', views.search_by_category_image, name='search_by_category_image'),
    path(r'searchnovel/', views.search_by_category_novel, name='search_by_category_novel'),
    path(r'searchblog/', views.search_by_category_blog, name='search_by_category_blog'),
    path(r'test/', views.test_celery, name="test_celery")
]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
