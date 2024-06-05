import random
from django.core.cache import cache
from django.db.models import Count
from article.models import Article
from config import settings


def get_random_articles(count: int) -> list:
    queryset_count = Article.objects.aggregate(count=Count('id'))['count']

    if queryset_count == 0:
        random_articles = []
    elif count >= queryset_count:
        random_articles = list(Article.objects.all())
    else:
        random_indexes = random.sample(range(queryset_count), count)
        random_articles = [Article.objects.all()[index] for index in random_indexes]
    return random_articles


def get_random_articles_cache(count_article: int) -> list:
    if settings.CACHE_ENABLED:
        key = 'home_list'
        article_list = cache.get(key)
        if article_list is None:
            article_list = get_random_articles(count_article)
            cache.set(key, article_list)
    else:
        article_list = get_random_articles(count_article)

    return article_list


def get_article_list_from_cache():
    if settings.CACHE_ENABLED:
        key = 'article_list'
        article_list = cache.get(key)
        if article_list is None:
            article_list = Article.objects.all()
            cache.set(key, article_list)
    else:
        article_list = Article.objects.all()

    return article_list
