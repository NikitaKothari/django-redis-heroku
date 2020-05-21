from django.conf import settings
import redis

POOL = redis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=settings.LIMIT, timeout=100)
