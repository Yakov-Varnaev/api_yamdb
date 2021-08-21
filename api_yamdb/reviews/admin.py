from django.contrib import admin

from .models import Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'pub_date', 'title')
    search_fields = ('title', 'author', 'pub_date')
    empty_display = '--empty--'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'review', 'pub_date')
    search_fields = ('author', 'pub_date')
    empty_display = '--empty--'
