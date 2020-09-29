from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.article.models import ArticlePost

# Create your views here.
from .forms import CommentPostForm


@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)

    if request.method == 'POST':
        comment_form = CommentPostForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            # 利用model对象调用一个内置函数来实现重定向
            return redirect(article)
            # return redirect("article:article_detail", id=article_id)该方法是之前修改文章使用的直接重定向方式
        else:
            return HttpResponse("评论信息有误，请重新填写")
    else:
        return HttpResponse("发表评论仅接受POST请求")
