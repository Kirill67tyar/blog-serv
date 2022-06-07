from django.contrib import admin
from blog.models import Post


# по простому так
# admin.site.register(Post)

# настроить так
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'author', 'publish', 'status',)
    list_filter = ('publish', 'author', 'created', 'status',)
    search_fields = ('title', 'body', 'slug', 'author__username',)
    prepopulated_fields = {'slug': ('title',)}  # поле которое автоматически преобразует slug в title
    raw_id_fields = ('author',) # благодаря этому атрибуту, появилась возможость искать автора не из списка
    date_hierarchy = 'publish' # ссылки для навигации по датам (под поиском)
    ordering = ('status', 'publish',)


"""
model fields:
    title
    slug
    author
    body
    publish
    created
    updated
    status
"""
