# main/signals.py
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.cache import cache
from . import models

ACCUEIL_CACHE_KEY = 'accueil_page_context_v1'


@receiver([post_save, post_delete], sender=models.article)
def clear_cache_on_article_change(sender, **kwargs):
    cache.delete(ACCUEIL_CACHE_KEY)


@receiver(m2m_changed, sender=models.article.cathegorie.through)
def clear_cache_on_article_cathegorie_change(sender, action, **kwargs):
    if action in ('post_add', 'post_remove', 'post_clear'):
        cache.delete(ACCUEIL_CACHE_KEY)


@receiver([post_save, post_delete], sender=models.cathegorie)
def clear_cache_on_cathegorie_change(sender, **kwargs):
    cache.delete(ACCUEIL_CACHE_KEY)


@receiver([post_save, post_delete], sender=models.cathegorie_cours)
def clear_cache_on_cathegorie_cours_change(sender, **kwargs):
    cache.delete(ACCUEIL_CACHE_KEY)