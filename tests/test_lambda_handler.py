import json
import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch("lambda_function.S3Service")
    @patch("lambda_function.RedisRepository")
    @patch("lambda_function.ZipProcessingUseCase")
    def test_lambda_handler_success(self, MockZipProcessingUseCase, MockRedisRepository, MockS3Service):
        mock_s3_service = MagicMock()
        mock_redis_repo = MagicMock()
        mock_use_case = MagicMock()

        mock_use_case.process_zip.return_value = "https://presigned-url.com"

        # Definindo o mock das classes
        MockS3Service.return_value = mock_s3_service
        MockRedisRepository.return_value = mock_redis_repo
        MockZipProcessingUseCase.return_value = mock_use_case

        event = {
            "queryStringParameters": {
                "S3Bucket": "my-bucket",
                "S3Path": "my-path",
                "FileName": "my-file.zip"
            }
        }
        context = {}

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("presigned_url", json.loads(response["body"]))
        self.assertEqual(json.loads(response["body"])["presigned_url"], "https://presigned-url.com")

    @patch("lambda_function.S3Service")
    @patch("lambda_function.RedisRepository")
    @patch("lambda_function.ZipProcessingUseCase")
    def test_lambda_handler_failure_missing_params(self, MockZipProcessingUseCase, MockRedisRepository, MockS3Service):
        event = {
            "queryStringParameters": {
                "S3Bucket": "my-bucket",
                "S3Path": "my-path"
            }
        }
        context = {}

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("error", json.loads(response["body"]))

if __name__ == "__main__":
    unittest.main()
