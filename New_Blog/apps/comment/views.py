from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.article.models import ArticlePost

# Create your views here.
from .forms import CommentPostForm
from .models import CommentPost


@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    # parent_comment_id为none即表示该评论为一级评论
    article = get_object_or_404(ArticlePost, id=article_id)

    if request.method == 'POST':
        comment_form = CommentPostForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = CommentPost.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级，root即为根级元素-一级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()
            # 利用model对象调用一个内置函数来实现重定向
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
        # return redirect("article:article_detail", id=article_id)该方法是之前修改文章使用的直接重定向方式

        # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentPostForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    else:
        return HttpResponse("发表评论仅接受GET/POST请求")
