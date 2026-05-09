from functools import wraps
from django.core.cache import cache

from rest_framework.request import Request

from rest_framework.response import Response
from ABCE.redis_client import redis_client, get_redis_connection


def clear_cache(pattern='order_list_*'):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            print(f"🗑️ ВЫЗВАН МЕТОД: {func.__name__}, очищаем {pattern}")  # 👈 добавить
            result = func(self, request, *args, **kwargs)
            
            try:
                redis = get_redis_connection("default")
                redis.delete_pattern(pattern)
                print(f"✅ Кэш очищен: {pattern}")
            except Exception as e:
                print(f"❌ Ошибка очистки: {e}")
            
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


def set_cache(pattern='user_', timeout=300):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request: Request, *args, **kwargs):
            cache_key = f"{pattern}{request.path}_{request.GET.urlencode()}"
            
            cached = cache.get(cache_key)
            if cached:
                return Response(cached)
            
            response = func(self, request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout)
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