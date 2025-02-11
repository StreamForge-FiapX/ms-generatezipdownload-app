import unittest
from unittest.mock import MagicMock
from infrastructure.s3_service import S3Service

class TestS3Service(unittest.TestCase):

    def test_list_zip_files(self):
        mock_s3_client = MagicMock()
        s3_service = S3Service()
        s3_service.s3_client = mock_s3_client

        mock_s3_client.list_objects_v2.return_value = {
            "Contents": [{"Key": "file1.zip"}, {"Key": "file2.zip"}]
        }

        result = s3_service.list_zip_files("my-bucket", "my-path")
        self.assertEqual(result, ["file1.zip", "file2.zip"])

if __name__ == "__main__":
    unittest.main()
