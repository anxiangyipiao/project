from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import ImageTable, NovelTable,BlogPost
import random
import base64
from django.core.paginator import Paginator
from .form import UserLoginForm,UserRegistrationForm
from .models import User
import hashlib 
from random import sample
from .decorators import role_required, permission_required,login_required
#
from django.core.cache import cache
from django.views.decorators.cache import cache_page

#task
from .tasks import add

def test_celery(request):
     result = add.delay(3, 5)
     return HttpResponse(result.task_id + ' : ' + result.status)


# 
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required, permission_required


# index 页
@cache_page(60 * 1)  # 缓存 15 分钟
def index(request):

    random_images,random_novels = random_12_img_novel()
    random_image = get_random_image()
    return render(request, 'index.html', locals())

def random_12_img_novel():
    all_images = ImageTable.objects.all()
    random_images = sample(list(all_images), 12)
    random_images = [encoded_images(i) for i in random_images]
    
    all_novels = NovelTable.objects.all()
    random_novels = sample(list(all_novels), 12)
    # random_novels = NovelTable.objects.order_by('?')[:12]
    return random_images,random_novels

def get_random_image():
    images = ImageTable.objects.all()
    if images:
        return  encoded_images(random.choice(images))
   
def encoded_images(random_images):
    random_images.source = base64.b64encode(random_images.source).decode('utf-8')
    return random_images
   
@login_required()
def image_list(request):
    is_login = request.session.get('is_login')
    image_list = ImageTable.objects.all().order_by('id')  # 获取所有图片记录
    paginator = Paginator(image_list, 21)  # 每页显示 21 条记录
    page_number = request.GET.get('page')  # 获取当前页数，默认为第一页

    page_obj = paginator.get_page(page_number)  # 获取当前页的记录
    for image in page_obj:
        image.source = encoded_images(image).source 

    return render(request, 'image_list.html', {'page_obj': page_obj,"is_login":is_login})


def novel_list(request):
    novel_list = NovelTable.objects.all().order_by('id')  # 获取所有小说记录
    paginator = Paginator(novel_list, 21)  # 每页显示 21 条记录
    page_number = request.GET.get('page')  # 获取当前页数，默认为第一页

    page_obj = paginator.get_page(page_number)  # 获取当前页的记录

    return render(request, 'novel_list.html', {'page_obj': page_obj})

# @role_required('admin')
# @permission_required(['edits'])
def blog_list(request):

    blogs = BlogPost.objects.all().order_by('id')
    paginator = Paginator(blogs, 21)  # 每页显示 21 条记录
    page_number = request.GET.get('page')  # 获取当前页数，默认为第一页

    page_obj = paginator.get_page(page_number)  # 获取当前页的记录
    return render(request, 'blog_list.html', {'page_obj': page_obj})



def search_by_category_image(request):
    
    selected_category = request.GET.get('category', None)
    print(selected_category)
    if selected_category:
        contents = ImageTable.objects.filter(category=selected_category)
    else:
        contents = ImageTable.objects.all()

    paginator = Paginator(contents, 21)  # 每页显示 21 条记录
    page_number = request.GET.get('page')  # 获取当前页数，默认为第一页

    page_obj = paginator.get_page(page_number)  # 获取当前页的记录
    for image in page_obj:
        image.source = encoded_images(image).source 

    return render(request, 'search_by_category_image.html', {'page_obj': page_obj ,"category":selected_category})


def search_by_category_novel(request):
    selected_category = request.GET.get('category', None)

    if selected_category:
        contents = NovelTable.objects.filter(category=selected_category)
    else:
        contents = NovelTable.objects.all()

    paginator = Paginator(contents, 21)  # 每页显示 21 条记录
    page_number = request.GET.get('page')  # 获取当前页数，默认为第一页

    page_obj = paginator.get_page(page_number)  # 获取当前页的记录
  
    return render(request, 'search_by_category_novel.html', {'page_obj': page_obj ,"category":selected_category})


def search_by_category_blog(request):
    selected_category = request.GET.get('category', None)

    if selected_category:
        contents = BlogPost.objects.filter(category=selected_category)
    else:
        contents = BlogPost.objects.all()

    paginator = Paginator(contents, 21)  # 每页显示 21 条记录
    page_number = request.GET.get('page')  # 获取当前页数，默认为第一页

    page_obj = paginator.get_page(page_number)  # 获取当前页的记录
  
    return render(request, 'search_by_category_blog.html', {'page_obj': page_obj ,"category":selected_category})


def blog_detail(request,blog_id):

    blog = get_object_or_404(BlogPost, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})















# auth
# def user_login(request):
#     if request.session.get('is_login',None):
#         return redirect('index')
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)     
#             request.session['is_login'] = True
#             request.session['user_id'] = user.id
#             request.session['user_name'] = user.username
#             return redirect('index')
#         else:
#             return render(request, 'login.html', locals())
 
#     login_form = UserLoginForm()
#     return render(request, 'login.html', locals())  
def hash_code(s, salt='anxiangyipiao'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def user_login(request):

    if request.session.get('is_login',None):

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('index')
    
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username

                    next_url = request.GET.get('next')
                    if next_url:
                         return redirect(next_url)
                    
                    return redirect('index')
                                
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())
 
    login_form = UserLoginForm()
    return render(request, 'login.html', locals())  

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect('index')
    request.session.flush()
    # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('index')

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect('index')
    if request.method == "POST":
        register_form = UserRegistrationForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                # 当一切都OK的情况下，创建新用户
 
                new_user = User.objects.create()
                new_user.username = username
                new_user.password = password1
                new_user.save()
                return redirect('index')  # 自动跳转到登录页面
    register_form = UserRegistrationForm
    return render(request, 'register.html', locals())



