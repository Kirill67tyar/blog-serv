import markdown

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post

# from blog.models import Post

register = template.Library()


# simple_tag - дожен возвращать какое-то значение (как правило QS)
@register.simple_tag
def total_posts(count=5):
    return Post.published.count()


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(count=Count('comments')).order_by('-count')[:count]


# inclusion_tag - обязательно должен возвращать контекст из словаря,
# и ссылаться на шаблон, где этот контекст как-то будет распаковыываться
@register.inclusion_tag('blog/templates_for_inclusion_tags/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts, }


@register.filter(name='markdown')
def markdown_string(text):
    return mark_safe(markdown.markdown(text))
