import redis
from django.conf import settings

client = redis.from_url(settings.REDIS_URL, socket_keepalive=True, socket_timeout=30)