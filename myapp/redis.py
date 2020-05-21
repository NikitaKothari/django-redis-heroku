import redis
from django.conf import settings

POOL = redis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=settings.LIMIT)
client = redis.Redis(connection_pool=POOL, decode_responses=True, socket_connect_timeout=2, socket_timeout=2)
