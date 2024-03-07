import sched
import time
import requests
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from scraper.base_scraper import BaseScraper


class IstockScraper(BaseScraper):
    base_url = "https://www.istockphoto.com/search/2/image-film"
    image_repository_bucket = "scraped-images-b1"

    def __init__(self):
        self.start_page = 2
        super().__init__(self.base_url, self.image_repository_bucket)
        print("IstockScraper initialized")

    def scrape_images(self):
        try:
            self.image_meta_repository.open_db_connection()
            print("IstockScraper scrape method")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

            
            url = f"{self.base_url}?page={self.start_page}&phrase=headshot"
            driver.get(url)

            image_elements = driver.find_elements(By.TAG_NAME, 'img')
            print("image_elements", image_elements)
            for i, image_element in enumerate(image_elements):
                image_url = image_element.get_attribute('src')
                print("image_url", image_url)
                image_data = requests.get(image_url).content
                image_filename = self.generate_file_name()
                if not self.image_meta_repository.is_image_scraped(image_url):
                    self.image_repository.save_image(
                        image_data, image_filename)
                    self.image_meta_repository.save_image_meta(
                        image_url, self.website_url, "")
                    self.scraped_image_count += 1
                    print("increased image count", self.scraped_image_count)
            self.scrape_next_images()
            driver.quit()
        except Exception as e: 
            print("Exception", e)

    def scrape_next_images(self):
        if self.scraped_image_count <= self.batch_size:
            self.start_page += 1
            self.scroll_down(self.browser)
        else:
            print(f"Scraped {self.scraped_image_count} images successfully")
            sys.exit()

        

# # Create scheduler instance
# scheduler = sched.scheduler(time.time, time.sleep)

# # Schedule the function again after 300 seconds
# def scheduled_scraping():
#     print("Scheduled Scraping Started at:", time.ctime())
#     scraper = IstockScraper()
#     scraper.scrape()
#     scheduler.enter(300, 1, scheduled_scraping)

