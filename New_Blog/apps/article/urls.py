# Author Cuber
# coding=utf-8
# @Time    : 2020/8/22 13:15
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

# 引入path
from django.urls import path

# 正在部署的应用的名称
from apps.article import views

app_name = 'article'  # 指定应用名，在使用{% url ' ' %} 引用链接时就可以套用对应应用名下的模板

urlpatterns = [
    # path函数将url映射到视图
    path('article-list/', views.article_list, name='article_list'),
    # 文章归档
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    # 文章分类
    path('category-dist/<int:pk>', views.category, name='category'),
    # 文章标签
    path('tag-dist/<int:pk>', views.tag_dist, name='tag-dist'),
    # 文章详情
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),

]
