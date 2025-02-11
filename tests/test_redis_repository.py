import unittest
from unittest.mock import MagicMock
from infrastructure.redis_repository import RedisRepository

class TestRedisRepository(unittest.TestCase):

    def test_store_download_link(self):
        mock_redis_client = MagicMock()
        redis_repo = RedisRepository("localhost", 6379, None)
        redis_repo.redis_client = mock_redis_client

        redis_repo.store_download_link("my-file.zip", "https://presigned-url.com")

        mock_redis_client.hset.assert_called_with("zipdownload:my-file.zip", mapping={"presigned_url": "https://presigned-url.com"})

if __name__ == "__main__":
    unittest.main()
