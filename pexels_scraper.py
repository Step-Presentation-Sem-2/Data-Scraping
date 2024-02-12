from base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from botocore.exceptions import NoCredentialsError, BotoCoreError
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PexelsScraper(BaseScraper):
    website = "https://www.pexels.com/search/headshot/"
    image_repository_bucket = "scraped-images-b1"

    def __init__(self):
        super().__init__(self.website, self.image_repository_bucket)
        print("PexelsScraper init")

    def scrape_images(self):
        print("PexelScarper scrape_images")
        try:
            browser = self.init_web_driver()
            wait = WebDriverWait(browser, 10)
            self.save_pexel_images(browser, wait, self.website)
        except Exception as e:
            print("Exception", e)
