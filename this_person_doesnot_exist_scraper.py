import sys
import time
import requests
from base_scraper import BaseScraper


class ThisPersonDoesnotExistScraper(BaseScraper):
    website = "https://thispersondoesnotexist.com/"
    image_repository_bucket = "ai-generated-images-b1"

    def __init__(self):
        print("ThisPersonDoesnotExistScraper init")
        super().__init__(self.website, self.image_repository_bucket)

    def scrape_images(self):
        print("ThisPersonDoesnotExistScraper scrape_images")
        response = requests.get(self.website_url)
        if 200 <= response.status_code < 300:
            """In the case of https://thispersondoesnotexist.com/ we dont have the src attribute in HTML as the context 
            returned from the server a jpeg. So save MD5 hash of the image as the url"""
            image_hash = self.hash_bytes(response.content)
            self.save_image(response.content, image_hash, self.website, "")
            self.scraped_image_count += 1
            self.scrape_next_images()

    def scrape_next_images(self):
        if self.scraped_image_count <= self.batch_size:
            time.sleep(2)
            self.scrape_images()
        else:
            print(f"Scraped {self.scraped_image_count} images successfully")
            sys.exit()
