# Author Cuber
# coding=utf-8
# @Time    : 2020/10/1 15:31
# @Site    : 
# @File    : article_extras.py.py
# @Software: PyCharm

from django import template
from django.utils import timezone
import math

from ..models import ArticlePost, ArticleColumn, Tag
from django.db.models.aggregates import Count

register = template.Library()


# 用来注册过滤器的名称，如不添加则直接视函数名为过滤器的名称，更多filter的用法见官网学习
@register.filter(name='string_transfer')
def transfer(value):
    """将输出转换为字符串"""
    transferred = str(value)
    return transferred


# 获取相对时间
@register.filter(name='relate_time')
def relate_time(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and 0 <= diff.seconds < 60:
        # 即一分钟以内的
        return '刚刚'

    if diff.days == 0 and 60 <= diff.seconds < 3600:
        # 即一小时以内的，向下取整
        return str(math.floor(diff.seconds / 60)) + "分钟前"

    if diff.days == 0 and 3600 <= diff.seconds < 86400:
        # 即一天以内的
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if 1 <= diff.days < 30:
        return str(diff.days) + "天前"

    if 30 <= diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"


# 对文章点在量的分级展示
@register.filter(name='liked_level')
def liked_level(value):
    # 暂定100个赞为满电实现的条件
    if value <= 20:
        return 0  # 对应empty  0%
    elif 20 < value <= 40:
        return 1  # 对应quarter  15%
    elif 40 < value <= 60:
        return 2  # 对应half  50%
    elif 60 < value <= 80:
        return 3  # 对应three-quarter  75%
    else:
        return 4  # 对应full  100%


@register.inclusion_tag('article/inclusions/_show_likes_num.html', takes_context=True)
def show_likes_num(context, article):
    return {
        'article': article,
    }


@register.inclusion_tag('article/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': ArticlePost.objects.all().order_by('-created')[:num],
    }


@register.inclusion_tag('article/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': ArticlePost.objects.dates('created', 'month', order='DESC'),
    }


@register.inclusion_tag('article/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = ArticleColumn.objects.annotate(num_posts=Count('article')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('article/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('tag')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }


@register.inclusion_tag('article/inclusions/_show_share_link.html', takes_context=True)
def show_share_link(context):
    return None
