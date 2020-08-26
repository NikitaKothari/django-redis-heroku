import redis

from django.conf import settings

print(settings.REDIS_URL)
client = redis.from_url(settings.REDIS_URL)
