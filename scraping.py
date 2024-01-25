import os
import requests
import boto3
from datetime import datetime
from botocore.exceptions import NoCredentialsError, BotoCoreError
from dotenv import load_dotenv
load_dotenv()


class scrapingUsingAPI():

    """
    Input: API_Key
    Output: Images saved to the S3 Bucket
    """

    def __init__(self, api_key, api_url):

        self.api_key = api_key
        self.api_url = api_url
        self.bucket_name = os.getenv("s3_bucket_name")
        self.aws_access_key_id = os.getenv("aws_access_key_id"),
        self.aws_secret_access_key = os.getenv("aws_secret_access_key")
        self.headers = {
            'Authorization': self.api_key
        }

    def generate_file_name(self):
        current_time = datetime.now()
        time_in_format = current_time.strftime("%d-%m-%Y-%H-%M-%S-%f")
        file_name = f"{time_in_format}.jpg"
        return file_name

       

    def scrap_image(self, page, per_page):
        """
        This function uses the API Key to get a headshot image.
        """

        params = {
            'query': "headshot",
            'page': page,
            'per_page': per_page
        }

        response = requests.get(
            self.api_url, headers=self.headers, params=params)

        self.process_response(response)
        

    def process_response(self, response):
        """
        This function process the response and returns the images if the response is 200(Successfull)
        or else returns error if response is 404.
        """
        # check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Loop through each photo in the response
            for index, photo in enumerate(data['photos']):
                # try:
                url = photo['src']['original']
                # Make the request to download the image
                response = requests.get(url)
                """
                This method is a way to ensure that your program handles unexpected responses from an HTTP request properly.

                Here's how raise_for_status() works:
                After Making an HTTP Request: You typically call raise_for_status() on the response object you receive after making an HTTP request.
                Checks the HTTP Status Code: This method checks the HTTP status code of the response.
                Raises an Exception for 4XX and 5XX Status Codes: If the status code is an error code (usually in the 400 or 500 range), raise_for_status() will raise an HTTPError exception. This can be useful for error handling in your code, as it lets you detect and handle HTTP errors in a structured way.
                Does Nothing for 2XX Status Codes: If the status code indicates success (i.e., it's in the 200 range), the method does nothing and allows the program to continue execution.
                """
                response.raise_for_status()
                if response.content:
                    s3_file_name = self.generate_file_name()
                    if not self.save_image_to_S3_bucket(response.content, s3_file_name):
                        print(f"Failed to upload{url}")
                else:
                    print(f"Failed to fetch image from {url}")

                    # Save the content into S3 bucket
                # except Exception as e:
                #     print("Error processing image number {}".format(index))

    def save_image_to_S3_bucket(self, image_content, s3_file_name):
        """
        saves the image to S3 bucket instance
        """
        # Create a S3 client
        print("keys", self.aws_access_key_id, self.aws_secret_access_key)
        s3 = boto3.client(
            "s3",
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key
        )

        try:
            s3.put_object(Body=image_content,
                          Bucket=self.bucket_name, Key=s3_file_name)
            print(f"Image uploaded to {self.bucket_name}/{s3_file_name}")
            return True

        except NoCredentialsError:
            print("Credentials not available")
            return False


def automated_scraping():
    """
    A function that scrapes images and saves them in an AWS S3 bucket Automatically.
    """
    # Creating a scrapingUsingAPI instance
    scrap_using_api = scrapingUsingAPI(api_url='https://api.pexels.com/v1/search',
                                       api_key='7Ebv0WB9C1ThJK6hxRxNpX9akqF1QKnb0qBFF4jVITwxdPl4cIlRoe7s')
    page=1
    per_page=15
    # Default Condition to check
    while True:
        if scrap_using_api.scrap_image(page,per_page):
            
            page+=1
        else:
            print("invalid")

    # scrap_using_api.scrap_image(page,per_page )


automated_scraping()
