from django.contrib import admin
from .models import BlogArticle

class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish')
    list_filter = ('publish', 'author')
    search_fields = ('author', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['publish', 'author']

admin.site.register(BlogArticle, BlogArticleAdmin)
