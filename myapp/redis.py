import redis
from django.conf import settings
import structlog

log = structlog.get_logger()
log.info("*******************")
log.info(settings.REDIS_URL)
log.info("*******************")


POOL = redis.ConnectionPool.from_url(settings.REDIS_URL)
client = redis.Redis(connection_pool=POOL, decode_responses=True)
