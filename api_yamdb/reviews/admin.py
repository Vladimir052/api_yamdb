from django.contrib import admin

from .models import Categories, Comment, Genres, Reviews, Titles, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')
    list_filter = ('role', )
    search_fields = ('username__startswith', )


@admin.register(Categories)
class Categoriesdmin(admin.ModelAdmin):
    search_fields = ("name__startswith", )


@admin.register(Genres)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name__startswith", )


@admin.register(Titles)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    list_filter = ("year", )
    search_fields = ("name__startswith", )


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ("text", )
    list_filter = ("author", )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ("text", )
    list_filter = ("author", )
