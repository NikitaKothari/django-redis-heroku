import redis
from django.conf import settings

import structlog
log = structlog.get_logger()


log.info("*******************************")
log.info(settings.REDIS_URL)
log.info("*******************************")

client = redis.from_url(settings.REDIS_URL)