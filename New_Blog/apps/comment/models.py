from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from apps.article.models import ArticlePost

from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


class CommentPost(MPTTModel):
    # 必要元素，用来保存评论之间的数据结构
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children'
                            )
    # 记录二级评论回复的对象，即一级评论的用户对象
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='repliers'
    )

    # 被评论的文章，注意他们与其他模型的关系
    article = models.ForeignKey(ArticlePost,
                                on_delete=models.CASCADE,
                                related_name='comments'
                                )
    # 评论者
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="comments"
                             )
    # related_name是用来通过主表查询外表调用数据是定义的外键名（不做修改时，默认是:子表名_set）

    comment_body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    # auto_now_add 指的是初次修改的时间，不可再次被修改；auto_now则指的是最后一次修改的时间，可以不断更新

    class MPTTMeta:
        ordering_insertion_by = ['created']

    def __str__(self):
        return self.comment_body[:30]
