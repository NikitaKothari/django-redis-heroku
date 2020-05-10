import redis

from django.conf import settings

print("******************************************")
print(settings.LIMIT)
print("******************************************")

POOL = redis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=settings.LIMIT)