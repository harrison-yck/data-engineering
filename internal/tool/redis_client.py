import redis as redis


class RedisClient:
    def __init__(self, redis_config):
        self.redis = redis.StrictRedis(**redis_config)

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value):
        return self.redis.set(key, value)
    