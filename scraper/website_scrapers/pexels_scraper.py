import requests
import time
import sys
from scraper.base_scraper import BaseScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class PexelsScraper(BaseScraper):
    website = "https://www.pexels.com/search/headshot/"
    image_repository_bucket = "scraped-images-b1"

    def __init__(self):
        super().__init__(self.website, self.image_repository_bucket)
        print("PexelsScraper init")

    def scrape_images(self):
        print("PexelScarper scrape_images")
        try:
            self.image_meta_repository.open_db_connection()
            wait = WebDriverWait(self.browser, 10)

            while self.new_image_count < self.max_new_image_count:
                self.scrape_next_images()
                # Ensure the column div is present before proceeding to find images within it
                column_div = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div[data-testid="column"]'))
                )
                # Find all image by tag "img"
                images = column_div.find_elements(By.TAG_NAME, 'img')

                # Track whether new images are found
                new_image_found = False

                # Download each image and save the url to found_image
                for img in images:
                    img_url = img.get_attribute('src')
                    if img_url:
                        try:
                            img_data = requests.get(img_url).content
                            img_filename = self.generate_file_name()
                            if not self.image_meta_repository.is_image_scraped(img_url):
                                print("Image data scraped:", img_url)
                                self.image_repository.save_image(
                                    img_data, img_filename)
                                self.image_meta_repository.save_image_meta(
                                    img_url, self.website_url, "")
                                new_image_found = True
                                self.scraped_image_count += 1

                        except Exception as e:
                            print(
                                "failed to download image at {img_url} : {e}")

                if not new_image_found:
                    self.new_image_count += 1
                else:
                    self.new_image_count = 0

            self.image_meta_repository.close_db_connection()

        except Exception as e:
            time.sleep(10)
            self.scrape_next_images()
            print("Exception occured in scrape_images")

    def scrape_next_images(self):
        print("Scraped Next Image called")
        if self.scraped_image_count <= self.batch_size:
            self.scroll_down(self.browser)
        else:
            print(f"Scraped {self.scraped_image_count} images successfully")
            sys.exit()
