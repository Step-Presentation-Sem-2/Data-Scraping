import os
import validators
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
    batch_size = 200
    scraped_image_count = 0
    headless_browser = None

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

    def init_web_driver(self):
        print("init_web_driver")

        driver_path = os.getenv("driver_path")

        chrome_options = Options()
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.headless = True
        chrome_options.add_argument("--window-size=1920,1200")

        service = Service(executable_path=driver_path)
        self.headless_browser = webdriver.Chrome(service=service, options=chrome_options)

    def save_image(self, image: bytes, url: str, host: str, e_tag: str):
        self.image_meta_repository.open_db_connection()
        if not (url.endswith(".jpeg") or url.endswith(".png") or url.endswith(".jpg") or url.endswith(".webp")):
            url = url + ".jpeg"
        if not self.image_meta_repository.is_image_scraped(url):
            self.image_repository.save_image(image, url)
            self.image_meta_repository.save_image_meta(url, host, e_tag)
        self.image_meta_repository.close_db_connection()
