import redis
from myapp.pool import POOL

client = redis.Redis(host="localhost", port=6201, password='p39d87357fb2861c9b82d0f3e682ffd01d56ae6f26ed2bdd84bbd65bfaecbd1bf')
