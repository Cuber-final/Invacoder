import re

# Create your views here.

# 视图函数
# 引入markdown模块
import markdown
# 导入数据模型ArticlePost
from apps.comment.forms import CommentPostForm
from .models import ArticlePost, ArticleColumn

# 引入redirect重定向模块
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm

# 引入评论表单类

from apps.comment.models import CommentPost
# 引入User模型
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.db.models import Q


# class ArticleListView(ListView):
#     context_object_name = 'articles'
#
#     queryset = ArticlePost.objects.all()
#
#     template_name = 'article/list.html'


def article_list(request):
    # 根据GET请求中查询条件
    # 返回按照不同要求排序的对象数组

    search = request.GET.get('search')
    order = request.GET.get('order')
    # 联合查询逻辑
    if search:
        if order == 'views_rank':

            articles_list = ArticlePost.objects.filter(Q(title__icontains=search) | Q(body__icontains=search)).order_by(
                '-total_views')
        else:
            articles_list = ArticlePost.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
    else:
        # search不设置为空则会被识别为'None'字符串，这样就依然会触发关键词搜索的效果
        search = ''
        if order == 'views_rank':
            # 根据GET获取的order参数将文章按照浏览数由大到小逆序组织
            articles_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            articles_list = ArticlePost.objects.all()
    # 每页显示4篇文章
    paginator = Paginator(articles_list, 4)
    # 获取 url 中的页码
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    # 将导航对象相应的页码内容返回给 articles
    context = {'articles': articles, 'order': order, 'search': search}
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # 取出所有评论

    # 注意括号里的参数article=id
    # 其实指的是CommentPost对象中的article其作为article的外键对应的article_id=id
    comments = CommentPost.objects.filter(article=id)

    if article.author != request.user:
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
        ])

    # 将正文按照md语法渲染为html页面，同时实现了能够单独提取目录变量
    article.body = md.convert(article.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    md.toc = m.group(1) if m is not None else ''

    comment_form = CommentPostForm()
    context = {'article': article, 'toc': md.toc, 'comments': comments, 'comment_form': comment_form, }
    return render(request, 'article/detail.html', context)


# 写文章的视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)

            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()

        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/create.html', context)


# 删文章
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")


# 安全删除文章
def article_safe_delete(request, id):
    # 验证表单传递，由于在detail里写的请求方法为post，所以要两边验证，再进行安全删除
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.user != article.author:
        return HttpResponse("抱歉，您无权修改此文章!")

    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']

            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        # 将旧原文信息保存在old_context中,添加参数intiall将旧数据传递到表单里
        old_context = {'title': article.title, 'body': article.body}

        columns = ArticleColumn.objects.all()
        article_post_form = ArticlePostForm(initial=old_context)
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article,
                   'article_post_form': article_post_form,
                   'columns': columns}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


def homepage(request):
    return render(request, 'Home.html')
