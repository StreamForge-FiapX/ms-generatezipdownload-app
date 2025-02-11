import boto3
import zipfile
from domain.repositories import S3ServiceInterface

class S3Service(S3ServiceInterface):
    def __init__(self):
        self.s3_client = boto3.client('s3')
    def list_zip_files(self, bucket, path):
        response = self.s3_client.list_objects_v2(Bucket=bucket, Prefix=path)
        return [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.zip')]
    def create_zip(self, zip_keys, file_name):
        zip_path = f"/tmp/{file_name}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as final_zip:
            for key in zip_keys:
                data = self.s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()
                final_zip.writestr(key.split('/')[-1], data)
        return zip_path
    def upload_zip(self, bucket, path, zip_path):
        output_key = f"{path}/generated-zips/{os.path.basename(zip_path)}"
        self.s3_client.upload_file(zip_path, bucket, output_key)
        return output_key
    def generate_presigned_url(self, bucket, key):
        return self.s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=3600)
