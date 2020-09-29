# Author Cuber
# coding=utf-8
# @Time    : 2020/9/7 19:24
# @Site    : 
# @File    : forms.py
# @Software: PyCharm
from django import forms

from .models import CommentPost


class CommentPostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = CommentPost
        # 定义表单包含的字段
        fields = ['comment_body']