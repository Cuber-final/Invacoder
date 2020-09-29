# Author Cuber
# coding=utf-8
# @Time    : 2020/8/23 14:50
# @Site    :
# @File    : forms.py
# @Software: PyCharm

from django import forms

from django.contrib.auth.models import User

# 对于与用户而非管理的这类对象，不需要慧姐对数据库进行交互改动的，通过集成forms.Form来自行配置字段信息
# 对于管理员则通过继承forms.ModelForm
from .models import Profile


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # 引用父类的cleaned_data()方法
        data = self.cleaned_data

        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试。")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
