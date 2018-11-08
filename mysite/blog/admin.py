from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from .models import Category, Comment, Post

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content_text',)

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post, PostAdmin)