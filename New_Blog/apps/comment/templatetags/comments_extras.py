# Author Cuber
# coding=utf-8
# @Time    : 2020/10/4 8:36
# @Site    : 
# @File    : comments_extras.py
# @Software: PyCharm


from django import template
from ..forms import CommentPostForm
from ..models import CommentPost

register = template.Library()


# 模板标签将表单数据等交给自定义的模板进行渲染
@register.inclusion_tag('comment/inclusions/_commentPost.html', takes_context=True)
def show_comment_post(context, article, comment_form=None):
    if comment_form is None:
        comment_form = CommentPostForm()
    return {
        'comment_form': comment_form,
        'article': article,
    }


@register.inclusion_tag('comment/inclusions/_commentList.html', takes_context=True)
def show_comment_list(context, article, user, comments):
    return {
        'article': article,
        'user': user,
        'comments': comments
    }
