import os
import csv
import time
import requests
import boto3
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from botocore.exceptions import NoCredentialsError, BotoCoreError
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
load_dotenv()


class AutomatedScraping():
    """
    This class is responsible for automated web scraping of images from a specified URL,
    and uploading them to an AWS S3 bucket.
    """

    def __init__(self, url, driver_path):
        """
        Initializes the AutomatedScraping object with the URL to scrape from, and the path to the webdriver.
        :input url: URL of the website to scrape images from.
        :input driver_path: File path to the Selenium WebDriver.
        """

        self.url = url
        self.driver_path = driver_path
        # To keep track of URL to avoid duplicate image being uploaded
        self.found_images = set()
        self.new_image_count = 0  # Counter to scroll without new images
        self.max_new_image_count = 3  # Max no of scrolls without new image before breaking
        self.bucket_name = os.getenv("s3_bucket_name")
        self.aws_access_key_id = os.getenv("aws_access_key_id")
        self.aws_secret_access_key = os.getenv("aws_secret_access_key")

    def generate_file_name(self):
        """
        Generates a unique file name based on the current datetime.
        :output: A string representing the file name.
        """
        current_time = datetime.now()
        time_in_format = current_time.strftime("%d-%m-%Y-%H-%M-%S-%f")
        file_name = f"{time_in_format}.jpg"
        return file_name

    def start_session(self):
        """
        Starts a new Selenium browser session.
        :output: An instance of a Selenium browser.
        """
        chrome_options = Options()
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        service = Service(executable_path=self.driver_path)
        browser = webdriver.Chrome(service=service, options=chrome_options)
        browser.get(self.url)
        return browser

    def scroll_down(self, browser):
        """
        Scrolls down the webpage in the given browser session.
        :input browser: The Selenium browser instance.
        """
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Let the page load

    def save_image_metadata_to_csv(self, img_url, img_filename, s3_path):
        csv_file = 'image_metadata.csv'
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Image URL', 'Image Filename', 'S3 Path'])
            writer.writerow([img_url, img_filename, s3_path])

        print(f"Metadata for {img_filename} saved to CSV.")

    def scrape_image(self):
        """
        Main method to start the image scraping process. 
        Scrolls through the webpage and downloads new images.
        If no new image is found break the loop and quit the browser
        """
        try:
            browser = self.start_session()
            wait = WebDriverWait(browser, 10)  # waits for up to 10 seconds
            while self.new_image_count < self.max_new_image_count:
                # scroll down the page
                self.scroll_down(browser)

                # Find all image by tag "img"
                images = wait.until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))

                # Track whether new images are found
                new_image_found = False

                # Download each image and save the url to found_image
                for img in images:
                    img_url = img.get_attribute('src')
                    print(img_url)
                    if img_url and img_url not in self.found_images:
                        try:

                            img_data = requests.get(img_url).content
                            img_filename = self.generate_file_name()
                            s3_path = self.save_image_to_S3_bucket(
                                img_data, img_filename)
                            if s3_path:
                                self.save_image_metadata_to_csv(
                                    img_url, img_filename, s3_path)
                                self.found_images.add(img_url)
                                new_image_found = True

                        except Exception as e:
                            print(
                                "failed to download image at {img_url} : {e}")

                if not new_image_found:
                    self.new_image_count += 1
                else:
                    self.new_image_count = 0

        except Exception as e:
            print("Couldn't parse the image, {e}")
            browser.quit()

        # browser.quit()

    def save_image_to_s3_bucket(self, image_content, s3_file_name):
        """
        Saves the downloaded image to an S3 bucket.

        :input image_content: The content of the image to be saved.
        :input s3_file_name: The name of the file to be saved in the S3 bucket.
        :Output: True if upload is successful, False otherwise.
        """

        # Create a S3 client
        print("keys", self.aws_access_key_id, self.aws_secret_access_key)
        s3 = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

        try:
            s3_path = f"{self.bucket_name}/{s3_file_name}"
            s3.put_object(Body=image_content,
                          Bucket=self.bucket_name, Key=s3_file_name)
            print(f"Image uploaded to {self.bucket_name}/{s3_file_name}")
            return s3_path

        except NoCredentialsError:
            print("Credentials not available")
            return False


url = os.getenv("url")
driver_path = os.getenv("driver_path")
automateScrape = AutomatedScraping(url, driver_path)
automateScrape.scrape_image()
