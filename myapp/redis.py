import redis
from django.conf import settings

POOL = redis.BlockingConnectionPool.from_url(settings.REDIS_URL, max_connections=settings.LIMIT, timeout=10)
client = redis.Redis(connection_pool=POOL, decode_responses=True, socket_connect_timeout=2, socket_timeout=2)
