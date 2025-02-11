import os
import json
import logging
from application.use_cases import ZipProcessingUseCase
from infrastructure.s3_service import S3Service
from infrastructure.redis_repository import RedisRepository

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        params = event.get("queryStringParameters", {})
        s3_bucket = params.get("S3Bucket")
        s3_path = params.get("S3Path")
        file_name = params.get("FileName")
        if not (s3_bucket and s3_path and file_name):
            raise ValueError("Missing required parameters: S3Bucket, S3Path, FileName")

        s3_service = S3Service()
        redis_host = os.environ.get("REDIS_HOST")
        redis_port = int(os.environ.get("REDIS_PORT", 6379))
        redis_password = os.environ.get("REDIS_PASSWORD", None)
        redis_repo = RedisRepository(redis_host, redis_port, redis_password)

        use_case = ZipProcessingUseCase(s3_service, redis_repo)
        presigned_url = use_case.process_zip(s3_bucket, s3_path, file_name)

        return {"statusCode": 200, "body": json.dumps({"presigned_url": presigned_url})}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
