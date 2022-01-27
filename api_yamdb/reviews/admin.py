from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'title', 'score', 'pub_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'review', 'pub_date')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
