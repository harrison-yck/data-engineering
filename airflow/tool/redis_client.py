import redis


class RedisClient:
    def __init__(self, key, config):
        self.key = key
        self.redis = redis.StrictRedis(**config)

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value):
        return self.redis.set(key, value)
