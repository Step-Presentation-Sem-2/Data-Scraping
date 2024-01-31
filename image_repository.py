import os
import boto3
from botocore.exceptions import NoCredentialsError


class ImageRepository:
    s3_client = None
    bucket_name = None

    def __init__(self, bucket_name):
        print("init")
        self.bucket_name = bucket_name
        self.init_s3_client()

    def save_image(self, image, object_name):
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

    def init_s3_client(self):
        print("init_s3_client")
        if self.s3_client:
            return self.s3_client
        else:
            aws_access_key_id = os.getenv("aws_access_key_id"),
            aws_secret_access_key = os.getenv("aws_secret_access_key")
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
