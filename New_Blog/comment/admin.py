from django.contrib import admin

# Register your models here.
from django.contrib import admin

from comment.models import CommentPost

admin.site.register(CommentPost)
