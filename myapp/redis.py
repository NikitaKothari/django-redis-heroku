import redis
from django.conf import settings

POOL = redis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=settings.LIMIT)
client = redis.Redis(connection_pool=POOL, decode_responses=True)
client.config_set("timeout", 100)
