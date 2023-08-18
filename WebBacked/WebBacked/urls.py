"""WebBacked URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from app import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'admin/', admin.site.urls),     #将 /admin/ 路径映射到 Django 管理后台。
    path(r'api/', include('app.urls')),  #将以 /api/ 开头的 URL 路径映射到名为 app 的应用程序的 URL 配置（通常在应用程序的 urls.py 文件中定义）
]
