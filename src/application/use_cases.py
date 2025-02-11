class ZipProcessingUseCase:
    def __init__(self, s3_service, redis_repo):
        self.s3_service = s3_service
        self.redis_repo = redis_repo

    def process_zip(self, s3_bucket, s3_path, file_name):
        zip_keys = self.s3_service.list_zip_files(s3_bucket, s3_path)
        final_zip_path = self.s3_service.create_zip(zip_keys, file_name)
        output_key = self.s3_service.upload_zip(s3_bucket, s3_path, final_zip_path)
        presigned_url = self.s3_service.generate_presigned_url(s3_bucket, output_key)
        self.redis_repo.store_download_link(file_name, presigned_url)
        return presigned_url
