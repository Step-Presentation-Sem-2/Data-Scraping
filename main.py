from scraper.image_scraper_factory import ImageScraperFactory
from scraper.image_source import ImageSource
from scraper.website_scrapers.pexels_scraper import PexelsScraper
from dotenv import load_dotenv

load_dotenv()


def main():
    scraper_factory = ImageScraperFactory()
    # this_person_doesnot_exist_scraper = scraper_factory.get_scraper(
    #     ImageSource.THIS_PERSON_DOESNOT_EXIST)
    # this_person_doesnot_exist_scraper.scrape_images()

    # pexel_scraper = scraper_factory.get_scraper(ImageSource.PEXELS)
    # pexel_scraper.scrape_images()
    pexel_scraper = PexelsScraper()
    pexel_scraper.scrape_images()


main()
