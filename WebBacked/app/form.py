from django import forms
from .models import User
from captcha.fields import CaptchaField

class UserLoginForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=128)
    password = forms.CharField(label="密码",max_length=128,widget=forms.PasswordInput)
    captcha = CaptchaField(label='验证码')

class UserRegistrationForm(forms.Form):
    
    username = forms.CharField(label="用户名",max_length=128)
    password1 = forms.CharField(label="密码",max_length=128,widget=forms.PasswordInput)
    password2 = forms.CharField(label="密码",max_length=128,widget=forms.PasswordInput)
    captcha = CaptchaField(label='验证码')
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')