from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('id',)
    empty_value_display = '--empty--'


admin.site.register(User, UserAdmin)
