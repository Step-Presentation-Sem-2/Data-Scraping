# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import validators
import hashlib
from image_meta_repository import ImageMetaRepository
from image_repository import ImageRepository


def get_next_set_of_images():
    print("get next set of images")


class BaseScraper:
    """Base scraper class used which can be implemented by each of the image scraper"""

    website_url = ""
    image_meta_repository = ImageMetaRepository()
    image_repository = None
    batch_size = 200
    scraped_image_count = 0

    def __init__(self, scrape_website_url: str, image_repository_bucket: str):
        print("initializing BaseScraper")
        if validators.url(scrape_website_url):
            self.website_url = scrape_website_url
            self.init_web_driver()
        else:
            raise Exception("Invalid URL")

        self.image_repository = ImageRepository(image_repository_bucket)

    def init_web_driver(self):
        print("init_web_driver")
        # webdriver_options = Options()
        # webdriver_options.headless = True
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver.get(self.website_url)

    def scrape_images(self):
        print("scrape_images")

    def scrape_next_images(self):
        print("scrape_next_images")

    def save_image(self, image: bytes, url: str, host: str, e_tag: str):
        self.image_meta_repository.open_db_connection()
        if not (url.endswith(".jpeg") or url.endswith(".png") or url.endswith(".jpg") or url.endswith(".webp")):
            url = url + ".jpeg"
        if not self.image_meta_repository.is_image_scraped(url):
            self.image_repository.save_image(image, url)
            self.image_meta_repository.save_image_meta(url, host, e_tag)
        self.image_meta_repository.close_db_connection()

    def hash_bytes(self, content: bytes):
        image_hash = hashlib.md5()
        image_hash.update(content)
        return image_hash.hexdigest()
