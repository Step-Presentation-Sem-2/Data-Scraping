import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class IstockScraper(BaseScraper):
    base_url = "https://www.istockphoto.com/search/2/image-film"
    image_repository_bucket = "scraped-images-b2"

    def __init__(self):
        super().__init__(self.base_url, self.image_repository_bucket)
        print("IstockScraper initialized")

    def scrape(self):
        print("IstockScraper scrape method")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        start_page = 2
        end_page = 200

        for current_page in range(start_page, end_page + 1):
            url = f"{self.base_url}?page={current_page}&phrase=headshot"
            driver.get(url)

            image_elements = driver.find_elements(By.TAG_NAME, 'img')
            for i, image_element in enumerate(image_elements):
                image_url = image_element.get_attribute('src')
                if image_url:
                    file_name = f"image_{current_page}_{i}.jpg"

        driver.quit()

# Scraper Factory
class ScraperFactory:
    @staticmethod
    def get_scraper(scraper_type):
        if scraper_type == 'image':
            return IstockScraper()
        else:
            raise ValueError("Unknown scraper type")
