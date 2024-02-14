import os
import validators
import time
from datetime import datetime
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from image_repository.image_meta_repository import ImageMetaRepository
from image_repository.image_repository import ImageRepository


class BaseScraper(ABC):
    """Base scraper class used which can be implemented by each of the image scraper"""

    website_url = ""
    image_meta_repository = None
    image_repository = None
    batch_size = 50
    scraped_image_count = 0
    headless_browser = None
    new_image_count = 0  # Counter to scroll without new images
    max_new_image_count = 3  # Max no of scrolls without new image before breaking
    driver_path = os.getenv("driver_path")

    def __init__(self, scrape_website_url: str, image_repository_bucket: str):
        print("initializing BaseScraper")
        if validators.url(scrape_website_url):
            self.website_url = scrape_website_url
            self.init_web_driver()
        else:
            raise Exception("Invalid URL")

        self.image_repository = ImageRepository(image_repository_bucket)
        self.image_meta_repository = ImageMetaRepository()

    @abstractmethod
    def scrape_images(self):
        pass

    @abstractmethod
    def scrape_next_images(self):
        pass

    def generate_file_name(self):
        """
        Generates a unique file name based on the current datetime.
        :output: A string representing the file name.
        """
        current_time = datetime.now()
        time_in_format = current_time.strftime("%d-%m-%Y-%H-%M-%S-%f")
        file_name = f"{time_in_format}.jpg"
        return file_name

    def init_web_driver(self) -> None:
        """
        Starts a new Selenium browser session.
        :output: None
        """
        print("init_web_driver")
        driver_path = os.getenv("driver_path")

        chrome_options = Options()
        chrome_options.add_argument("--ignore-ssl-errors=yes")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.headless = True
        chrome_options.add_argument("--window-size=1920,1200")

        service = Service(executable_path=driver_path)
        self.headless_browser = webdriver.Chrome(
            service=service, options=chrome_options
        )

    def scroll_down(self):
        """
        Scrolls down the webpage in the given browser session.
        :input browser: The Selenium browser instance.
        """
        self.headless_browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(5)  # Let the page load

    def save_image(self, image: bytes, url: str, host: str, e_tag: str):
        self.image_meta_repository.open_db_connection()
        if not (
                url.endswith(".jpeg")
                or url.endswith(".png")
                or url.endswith(".jpg")
                or url.endswith(".webp")
        ):
            url = url + ".jpeg"
        if not self.image_meta_repository.is_image_scraped(url):
            self.image_repository.save_image(image, url)
            self.image_meta_repository.save_image_meta(url, host, e_tag)
        self.image_meta_repository.close_db_connection()
