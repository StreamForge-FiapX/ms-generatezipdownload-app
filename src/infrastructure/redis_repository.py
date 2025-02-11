import redis
from domain.repositories import RedisRepositoryInterface

class RedisRepository(RedisRepositoryInterface):
    def __init__(self, host, port, password):
        self.redis_client = redis.Redis(host=host, port=port, password=password, decode_responses=True)
    def store_download_link(self, file_name, url):
        redis_key = f"zipdownload:{file_name}"
        self.redis_client.hset(redis_key, mapping={"presigned_url": url})
