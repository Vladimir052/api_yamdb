from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')
    list_filter = ('role', )
    search_fields = ('username__startswith', )
