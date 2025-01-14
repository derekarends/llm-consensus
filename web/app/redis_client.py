import redis
import json

from __init__ import settings


class RedisClient:
    def __init__(self, db=0):
        self.client = redis.StrictRedis(
            host=settings.redis_host, port=settings.redis_port, db=db, decode_responses=True
        )

    def set(self, key, value):
        self.client.set(key, json.dumps(value))

    def get(self, key):
        res = self.client.get(key)
        if res:
          return json.loads(str(res))
        return res

    def delete(self, key):
        self.client.delete(key)
