# Author Cuber
# coding=utf-8
# @Time    : 2020/10/1 15:31
# @Site    : 
# @File    : article_extras.py.py
# @Software: PyCharm

from django import template

from ..models import ArticlePost, ArticleColumn, Tag
from django.db.models.aggregates import Count

register = template.Library()


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
