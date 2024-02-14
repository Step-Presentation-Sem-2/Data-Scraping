from dotenv import load_dotenv
from scraper.image_scraper_factory import ImageScraperFactory
from scraper.image_source import ImageSource

load_dotenv()


def main():
    scraper_factory = ImageScraperFactory()
    this_person_doesnot_exist_scraper = scraper_factory.get_scraper(ImageSource.THIS_PERSON_DOESNOT_EXIST)
    this_person_doesnot_exist_scraper.scrape_images()


main()
