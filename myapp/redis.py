import redis
from myapp.pool import POOL

client = redis.Redis(connection_pool=POOL, decode_responses=True)