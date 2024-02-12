from image_scraper_factory import ImageScraperFactory
from image_source import ImageSource
from pexels_scraper import PexelsScraper


def main():
    # scraper_factory = ImageScraperFactory()
    # this_person_doesnot_exist_scraper = scraper_factory.get_scraper(ImageSource.THIS_PERSON_DOESNOT_EXIST)
    # this_person_doesnot_exist_scraper.scrape_images()

    # pexel_scraper = scraper_factory.get_scraper(ImageSource.PEXELS)
    # pexel_scraper.scrape_images()
    PexelsScraper().scrape_images()


main()
