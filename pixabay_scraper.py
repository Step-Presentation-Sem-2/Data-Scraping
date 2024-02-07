import urllib.request, io
from base_scraper import BaseScraper


class PixabayScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        print("PexelsScraper init")

    def scrape_images(self):
        self.save_image()
