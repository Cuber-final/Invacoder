# Author Cuber
# coding=utf-8
# @Time    : 2020/8/23 15:15
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),

    # 用户退出
    path('logout/', views.user_logout, name='logout'),

    # 用户注册
    path('register/', views.user_register, name='register'),

    # 用户删除
    path('delete/<int:id>', views.user_delete, name='delete'),

    path('edit/<int:id>/', views.profile_edit, name='edit'),
]
