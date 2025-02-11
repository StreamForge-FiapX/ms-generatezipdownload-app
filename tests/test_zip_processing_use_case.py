import unittest
from unittest.mock import MagicMock
from application.use_cases import ZipProcessingUseCase

class TestZipProcessingUseCase(unittest.TestCase):

    def test_process_zip_success(self):
        mock_s3_service = MagicMock()
        mock_redis_repo = MagicMock()
        mock_use_case = ZipProcessingUseCase(mock_s3_service, mock_redis_repo)

        mock_s3_service.list_zip_files.return_value = ["zip1.zip", "zip2.zip"]
        mock_s3_service.create_zip.return_value = "/tmp/final.zip"
        mock_s3_service.upload_zip.return_value = "generated-zips/final.zip"
        mock_s3_service.generate_presigned_url.return_value = "https://presigned-url.com"

        result = mock_use_case.process_zip("my-bucket", "my-path", "my-file.zip")

        self.assertEqual(result, "https://presigned-url.com")
        mock_s3_service.list_zip_files.assert_called_with("my-bucket", "my-path")
        mock_s3_service.create_zip.assert_called()
        mock_s3_service.upload_zip.assert_called()
        mock_s3_service.generate_presigned_url.assert_called()

if __name__ == "__main__":
    unittest.main()
