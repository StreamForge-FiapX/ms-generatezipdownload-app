from abc import ABC, abstractmethod
class S3ServiceInterface(ABC):
    @abstractmethod
    def list_zip_files(self, bucket, path):
        pass
    @abstractmethod
    def create_zip(self, zip_keys, file_name):
        pass
    @abstractmethod
    def upload_zip(self, bucket, path, zip_path):
        pass
    @abstractmethod
    def generate_presigned_url(self, bucket, key):
        pass

class RedisRepositoryInterface(ABC):
    @abstractmethod
    def store_download_link(self, file_name, url):
        pass
