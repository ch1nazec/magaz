from django.conf import settings
from ABCE.redis_client import redis_client


def delete_cache(pattern='user_*'):
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)