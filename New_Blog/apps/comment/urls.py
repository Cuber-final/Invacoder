# Author Cuber
# coding=utf-8
# @Time    : 2020/9/7 19:04
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.urls import path

from apps.comment import views

app_name = 'comment'

urlpatterns = [
    path('post_comment/<int:article_id>/', views.post_comment, name='post_comment'),

]
