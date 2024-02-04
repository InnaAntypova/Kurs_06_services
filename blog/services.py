from django.core.cache import cache

from blog.models import Article


def get_article_cache():
    """ Сервисная функция для кеширования списка статей в Блоге """
    key = 'client_list'
    article_list = cache.get(key)
    if article_list is None:
        article_list = Article.objects.all()
        cache.set(key, article_list)
    return article_list
