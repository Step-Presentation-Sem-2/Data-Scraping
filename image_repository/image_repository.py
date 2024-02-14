import os
import boto3
from botocore.exceptions import NoCredentialsError


class ImageRepository:
    s3_client = None
    bucket_name = None

    def __init__(self, bucket_name: str):
        print("init")
        self.bucket_name = bucket_name
        self.init_s3_client()

    def save_image(self, image: bytes, object_name: str):
        print("save_image")
        try:
            self.s3_client.put_object(Body=image,
                                      Bucket=self.bucket_name,
                                      Key=object_name)
            print(f"Image uploaded to {self.bucket_name}/{object_name}")
            return True

        except NoCredentialsError:
            print("Credentials not available")
            return False
        except Exception as e:
            print(e)
            return False

    def init_s3_client(self):
        print("init_s3_client")
        if self.s3_client:
            return self.s3_client
        else:
            aws_s3_access_key = os.getenv("aws_s3_access_key")
            aws_s3_secret_key = os.getenv("aws_s3_secret_key")
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_s3_access_key,
                aws_secret_access_key=aws_s3_secret_key
            )
