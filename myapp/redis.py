import redis

from django.conf import settings

POOL = redis.ConnectionPool.from_url(settings.REDIS_URL)
client = redis.from_url(connection_pool=POOL, decode_responses=True)