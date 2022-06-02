from django.contrib import admin

from .models import Editor, Tags, Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'editor']
    ordering = ['title']

# Register your models here.

admin.site.register(Editor)
admin.site.register(Tags)
admin.site.register(Article, ArticleAdmin)

