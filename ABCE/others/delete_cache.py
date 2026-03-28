from django.conf import settings


def delete_cache(pattern):
    for key in settings.REDIS_CLIENT.scan_iter(pattern):
        settings.REDIS_CLIENT.delete(key)