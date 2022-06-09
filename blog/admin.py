from django.contrib import admin
from blog.models import (Post, Comment, Tag, )


# по простому так
# admin.site.register(Post)

# настроить так
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'author', 'publish', 'status',)
    list_filter = ('publish', 'author', 'created', 'status',)
    search_fields = ('title', 'body', 'slug', 'author__username',)
    prepopulated_fields = {'slug': ('title',)}  # поле которое автоматически преобразует slug в title
    raw_id_fields = ('author',)  # благодаря этому атрибуту, появилась возможость искать автора не из списка
    date_hierarchy = 'publish'  # ссылки для навигации по датам (под поиском)
    ordering = ('status', 'publish',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = 'pk', 'post', 'author', 'created', 'active',
    list_filter = 'created', 'updated', 'active',
    search_fields = 'post', 'author__username', 'body',


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'slug',
    list_filter = 'post',
    search_fields = 'name', 'slug', 'post',
    prepopulated_fields = {'slug': ('name',)}
