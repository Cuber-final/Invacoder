import re

# 视图函数
# 引入markdown模块
import markdown
# 导入数据模型ArticlePost
from django.http import HttpResponse
from django.views import View
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

from apps.comment.forms import CommentPostForm
from .models import ArticlePost, ArticleColumn, Tag

# 引入redirect重定向模块
from django.shortcuts import render, get_object_or_404

# 引入评论表单类

from apps.comment.models import CommentPost

from django.core.paginator import Paginator

from django.db.models import Q


def article_list(request):
    # 根据GET请求中查询条件
    # 返回按照不同要求排序的对象数组

    search = request.GET.get('search')
    order = request.GET.get('order')
    # 联合查询逻辑
    if search:
        if order == 'views_rank':
            post_list = ArticlePost.objects.filter(Q(title__icontains=search) | Q(body__icontains=search)).order_by(
                '-total_views')
        else:
            post_list = ArticlePost.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
    else:
        # search不设置为空则会被识别为'None'字符串，这样就依然会触发关键词搜索的效果
        search = ''
        if order == 'views_rank':
            # 根据GET获取的order参数将文章按照浏览数由大到小逆序组织
            post_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            post_list = ArticlePost.objects.all()
    # 每页显示4篇文章
    paginator = Paginator(post_list, 4)
    # 获取 url 中的页码
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    # 将导航对象相应的页码内容返回给 articles
    context = {'articles': articles, 'order': order, 'search': search}
    # render函数：载入模板，并返回context对象
    return render(request, 'Home.html', context)


def archive(request, year, month):
    post_list = ArticlePost.objects.filter(created__year=year,
                                           created__month=month
                                           ).order_by('-created')
    date_list = [year, month]
    # 每页显示4篇文章
    paginator = Paginator(post_list, 4)
    # 获取 url 中的页码
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    # 将导航对象相应的页码内容返回给 articles
    context = {'articles': articles, 'chose_date': date_list}
    return render(request, 'Home.html', context)


def category(request, pk):
    cate = get_object_or_404(ArticleColumn, pk=pk)
    post_list = ArticlePost.objects.filter(column=cate).order_by('-created')
    # 每页显示4篇文章
    paginator = Paginator(post_list, 4)
    # 获取 url 中的页码
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    # 将导航对象相应的页码内容返回给 articles
    context = {'articles': articles, 'cate': cate}
    return render(request, 'Home.html', context)


def tag_dist(request, pk):
    cur_tag = get_object_or_404(Tag, pk=pk)
    post_list = ArticlePost.objects.filter(tags=cur_tag).order_by('-created')
    # 每页显示4篇文章
    paginator = Paginator(post_list, 4)
    # 获取 url 中的页码
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    # 将导航对象相应的页码内容返回给 articles
    context = {'articles': articles, 'cur_tag': cur_tag}

    return render(request, 'Home.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # 取出所有评论

    # 注意括号里的参数article=id
    # 其实指的是CommentPost对象中的article其作为article的外键对应的article_id=id
    comments = CommentPost.objects.filter(article=id)

    # if article.author != request.user:
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',

            'markdown.extensions.toc',

            TocExtension(slugify=slugify),
        ])

    # 将正文按照md语法渲染为html页面，同时实现了能够单独提取目录变量
    article.body = md.convert(article.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    md.toc = m.group(1) if m is not None else ''

    comment_form = CommentPostForm()
    context = {'article': article, 'toc': md.toc, 'comments': comments, 'comment_form': comment_form, }
    return render(request, 'article/detail.html', context)


# 点赞增长的类视图
class LikesRiseView(View):
    def post(request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes_num += 1
        article.save()
        return HttpResponse('success')

# def homepage(request):
#     return render(request, 'Home.html')
