import requests
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from scraper.base_scraper import BaseScraper


class UnsplashScraper(BaseScraper):
    website = "https://unsplash.com/s/photos/people-headshots"
    image_repository_bucket = "scraped-images-b1"

    def __init__(self):
        print("UnsplashScraper init")
        super().__init__(self.website, self.image_repository_bucket)
        self.new_image_found = False

    def scrape_images(self):
        print("UnsplashScraper scrape_images")

        try:
            self.image_meta_repository.open_db_connection()
            wait = WebDriverWait(self.headless_browser, 10)

            while self.new_image_count < self.max_new_image_count:
                self.scrape_next_images()

                images_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                              'div[data-test="search-photos-route"]')))
                images = images_container.find_elements(By.CSS_SELECTOR, 'img[data-test="photo-grid-masonry-img"]')
                self.save_images(images)

                if not self.new_image_found:
                    self.new_image_count += 1
                else:
                    self.new_image_count = 0

            self.image_meta_repository.close_db_connection()

        except Exception as e:
            print("Exception", e)

    def save_images(self, images: list[WebElement]):
        for img in images:
            img_url = img.get_attribute('src')
            if img_url:
                try:
                    img_data = requests.get(img_url).content
                    img_filename = self.generate_file_name()
                    print("Image scraped from:", img_url)
                    if not self.image_meta_repository.is_image_scraped(img_url):
                        self.image_repository.save_image(
                            img_data, img_filename)
                        self.image_meta_repository.save_image_meta(
                            img_url, self.website_url, "")
                        self.new_image_found = True
                        self.scraped_image_count += 1

                except Exception as e:
                    print(f"failed to download image at {img_url} : {e}")

    def scrape_next_images(self):
        if self.scraped_image_count <= self.batch_size:
            self.scroll_down()
        else:
            print(f"Scraped {self.scraped_image_count} images successfully")
