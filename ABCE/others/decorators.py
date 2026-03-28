from functools import wraps
from django.core.cache import cache
from django_redis import get_redis_connection
from rest_framework.response import Response
from django.conf import settings


def clear_cache(pattern='order_list_*'):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            print('Начало вызова')
            result = func(self, request, *args, **kwargs)
            
            try:
                for key in settings.REDIS_CLIENT.scan_iter(pattern):
                    settings.REDIS_CLIENT.delete(key)
            except AttributeError:
                pass
            return result
        return wrapper
    return decorator


def auto_clear_cache(pattern='order_list_*'):
    def decorator(cls):
        for action in ['create', 'destroy', 'update', 'partial_update']:
            
            if hasattr(cls, action):
                original = getattr(cls, action)
                setattr(cls, action, clear_cache(pattern)(original))
        return cls
    return decorator


def set_cache(pattern='order_list_', timeout=300):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            query = request.GET.urlencode()
            cache_key = f"{pattern}{query}" if query else pattern.rstrip('_')
            cache_data = cache.get(cache_key)

            if cache_data:
                return Response(cache_data)
            
            response = func(self, request, *args, **kwargs)
            cache.set(key=cache_key, value=response.data, timeout=timeout)
            return response
        return wrapper
    return decorator

def auto_set_cache(pattern='order_list_', timeout=300):
    def decorators(cls):
        action = 'list'

        if hasattr(cls, action):
            original = getattr(cls, action)
            wrapped = set_cache(pattern)(original)
            setattr(cls, action, wrapped)
            
        return cls
    return decorators