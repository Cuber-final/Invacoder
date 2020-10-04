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
    # 已有代码，处理一级回复，第二个(缺省)参数没有时默认为none，就是处理一级评论的
    path('post-comment/<int:article_id>', views.post_comment, name='post_comment'),
    # 新增代码，处理二级回复
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')

]
