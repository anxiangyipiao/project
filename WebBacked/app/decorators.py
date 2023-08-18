from functools import wraps
from django.shortcuts import redirect
from .models import User,Role,UserRole,RolePermission,Permission
from django.core.cache import cache


def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get('is_login'):
                try:
                    user_id = request.session.get('user_id')    
                    # user = User.objects.get(id=user_id)
                    userrole = UserRole.objects.get(user__id=user_id)          
                    if userrole.role.name == role_name :     
                         return view_func(request, *args, **kwargs)
                except (User.DoesNotExist, Role.DoesNotExist):
                    pass
            return redirect('login')  # 重定向到登录页面
        return _wrapped_view
    return decorator


def permission_required(required_permissions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get('is_login'):
                try:
                    user_id = request.session.get('user_id')
                    # user = User.objects.get(id=user_id)
                    roleid = UserRole.objects.get(user__id=user_id).role.id
                    rolepermissions = RolePermission.objects.filter(role__id=roleid)
                    
                    # 检查用户是否拥有所有所需权限
                    user_permissions = set(rolepermission.permission.name for rolepermission in rolepermissions)
                    
                    if set(required_permissions).issubset(user_permissions):
                        return view_func(request, *args, **kwargs)
                    
                except (User.DoesNotExist, Permission.DoesNotExist):
                    pass
            return redirect('login')  # 重定向到登录页面
        return _wrapped_view
    return decorator


def login_required():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get('is_login'):
                try:    
                    return view_func(request, *args, **kwargs)
                except (User.DoesNotExist, Role.DoesNotExist):
                    pass
            return redirect('login')  # 重定向到登录页面
        return _wrapped_view
    return decorator


def cache_view(timeout):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            cache_key = f"{view_func.__name__}:{request.user.id}"
            cached_data = cache.get(cache_key)
            if cached_data is None:
                result = view_func(request, *args, **kwargs)
                cache.set(cache_key, result, timeout=timeout)
            else:
                result = cached_data
            return result
        return _wrapped_view
    return decorator