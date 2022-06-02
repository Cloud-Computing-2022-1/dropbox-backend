import boto3
import uuid

from django.conf import settings

# S3과 통신하기 위한 파일, settings.py로부터 access key와 secret key, bucket name을 받아서 s3 클라이언트를 생성하고 통신.


class FileUpload:
    def __init__(self, client):
        self.client = client

    def upload(self, file):
        return self.client.upload(file)


class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        boto3_s3 = boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )
        self.s3_client = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file):
        try:
            file_id = str(uuid.uuid4())
            extra_args = {
                "ContentType": file.content_type,
                "ContentDisposition": f'attachment; filename="{file.name}"',
            }

            self.s3_client.upload_fileobj(file, self.bucket_name, file_id, ExtraArgs=extra_args)
            return (
                file_id,
                f"https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_id}",
            )  # 업로드 시 ap-northeast-2에 있는 s3 bucket에 저장하도록 지정, 업로드 완료 시 파일 id와 url 디비에 저장
        except:
            return None


# MyS3Client instance
s3_client = MyS3Client(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY, settings.S3_BUCKET_NAME)
