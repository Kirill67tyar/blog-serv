from django.contrib.sitemaps import Sitemap

from blog.models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'  # частота обновления страниц статей
    priority = 0.9  # степень их совпадения с тематикой сайта (max - 1)

    # объекты которые будут отображаться в карте сайта
    def items(self):
        return Post.published.all()

    # каждый объект из результата вызова items()
    # время последней модификации статьи
    def lastmod(self, obj):
        return obj.updated

    # @staticmethod
    # def lastmod(obj):
    #     return obj.updated
