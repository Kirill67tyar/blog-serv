from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from blog.utils import from_cyrilic_to_eng

User = get_user_model()


# создание нового менелжера
class PublishedManager(models.Manager):
    def get_queryset(self):
        query = super().get_queryset().filter(status='publish')
        return query


# или переопределение старого
# class PublishedManager(models.Manager):
#     def get_published(self):
#         return self.get_queryset().filter(status='publish')


class Post(models.Model):
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
    STATUS_CHOICE = (
        ('draft', 'Draft',),
        ('publish', 'Published',),
    )
    title = models.CharField(
        max_length=250, verbose_name='Заголовок'
    )
    slug = models.SlugField(
        max_length=250, unique=True,
        blank=True, null=True,
        unique_for_date='publish'  # что slug был уникальный для даты поля publish
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='blog_posts'
    )
    body = models.TextField(
        verbose_name='Статья'
    )
    publish = models.DateTimeField(
        default=timezone.now, verbose_name='Опубликована'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Создана'
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Изменена'
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE,
        default='draft', verbose_name='Статус'
    )
    # дополнительный менеджер объектов
    objects = models.Manager()
    published = PublishedManager()

    # или переопределённый менеджер объектов:
    # objects = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrilic_to_eng(str(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={
            'year': self.publish.year,
            'month': self.publish.month,
            'day': self.publish.day,
            'post': self.slug,
        })


class Comment(models.Model):
    post = models.ForeignKey(
        to='blog.Post', on_delete=models.CASCADE,
        related_name='comments', verbose_name='Пост'
    )
    author = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True,
        related_name='comments', blank=True, verbose_name='Автор'
    )
    body = models.CharField(
        max_length=255, verbose_name='Содержание комментария'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Создан'
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Изменён'
    )
    active = models.BooleanField(
        default=True, verbose_name='Состояние'
    )

    def __str__(self):
        return f'Comment by {self.author.username}, on {self.post} ({self.created})'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название тега')
    slug = models.CharField(max_length=50, verbose_name='Slug тега')
    post = models.ManyToManyField(to='blog.Post', related_name='tags')

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrilic_to_eng(str(self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:list_by_tag', kwargs={
            'slug_tag': self.slug,
        })

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
