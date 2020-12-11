from django.db import models

from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.urls import reverse
from django.utils import timezone
import markdown
from PIL import Image
# django-ckeditor

# 博客文章数据模型
from django.utils.html import strip_tags
from mdeditor.fields import MDTextField


class ArticleColumn(models.Model):
    # 栏目标题
    title = models.CharField('标题', max_length=100, blank=True)
    # 栏目创建时间
    created = models.DateTimeField('创建时间', default=timezone.now)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField('文章标签', max_length=20, blank=True)
    created = models.DateTimeField('创建时间', default=timezone.now)

    def __str__(self):
        return self.name


class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    # 定义foreignkey（即数据库的外键）以设置user对象与ArticlePost对象的关联（一对多）
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章所述栏目，一对多关系
    column = models.ForeignKey(ArticleColumn,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               # 自定义外键名称
                               related_name='article'
                               )
    # 多对多关系，文章与标签
    tags = models.ManyToManyField(Tag, verbose_name='标签', related_name='tag')
    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField('标题', max_length=100)
    # 文章内容主体
    body = MDTextField('正文')
    # 文章摘要，预浏览
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    # 文章标题图
    thumbnail = models.ImageField('文章标题图', upload_to='article/%Y%m%d/', blank=True)

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField('创建时间', default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField('更新时间', auto_now=True)
    # 文章浏览量
    total_views = models.PositiveIntegerField('浏览数', default=0)

    # 文章被点赞数
    likes_num = models.PositiveIntegerField('点赞数', default=0)

    # 内部类 class Meta 用于给 model 定义元数据，
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 将markdown文本渲染成html文本，然后过滤标签选出文字

        md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                           'markdown.extensions.codehilite', ])
        self.excerpt = strip_tags(md.convert(self.body)[:40])
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.thumbnail and not kwargs.get('update_fields'):
            image = Image.open(self.thumbnail)
            (x, y) = image.size
            new_x = 500  # 可修改
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.thumbnail.path, "png")

        return article

    class Meta:
        # ordering 指定模型返回的数据的排列顺序，是元组形式的
        # '-created' 表明数据应该以倒序排列，这样就能在调用数据时按照文章的最新更新显示
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title


def get_absolute_url(self):
    return reverse('article:article_detail', args=[self.id])
