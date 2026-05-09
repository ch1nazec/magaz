from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from django.core.cache import cache
from django_redis import get_redis_connection

def clear_product_cache():
    redis = get_redis_connection("default")
    if not redis.ping():
        print('Redis сдох')
        return

    for key in redis.scan_iter(match='product_list_*'):
        redis.delete(key)

@receiver(post_save, sender=Product)
def clear_cache_on_save(sender, instance, **kwargs):
    clear_product_cache()
    print("🗑️ Кэш очищен (сохранение продукта)")

@receiver(post_delete, sender=Product)
def clear_cache_on_delete(sender, instance, **kwargs):
    clear_product_cache()