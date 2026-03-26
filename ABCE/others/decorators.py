from functools import wraps
from django.core.cache import cache


def clear_cache(pattern='order_list_*'):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            result = func(self, request, *args, **kwargs)
            cache.delete_pattern(pattern)
            return result
        return wrapper