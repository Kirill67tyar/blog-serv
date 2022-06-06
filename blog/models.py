from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from blog.utils import from_cyrilic_to_eng

User = get_user_model()


class Post(models.Model):
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
        unique_for_date='publish'
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

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrilic_to_eng(str(self.title))
        super().save(*args, **kwargs)