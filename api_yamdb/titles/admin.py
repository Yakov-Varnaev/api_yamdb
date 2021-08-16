from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_display = '--empty--'

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_display = '--empty--'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year', 'rating', 'description',
    )
    search_fields = ('name', 'year', 'description')
    empty_display = '--empty--'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
