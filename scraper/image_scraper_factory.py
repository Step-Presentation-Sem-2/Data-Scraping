from scraper.image_source import ImageSource
from scraper.base_scraper import BaseScraper
from scraper.website_scrapers.pexels_scraper import PexelsScraper
from scraper.website_scrapers.pixabay_scraper import PixabayScraper
from scraper.website_scrapers.unsplash_scraper import UnsplashScraper
from scraper.website_scrapers.five_hundred_px_scraper import FiveHundredPxScraper
from scraper.website_scrapers.this_person_doesnot_exist_scraper import ThisPersonDoesnotExistScraper


class ImageScraperFactory:
    @staticmethod
    def get_scraper(source: ImageSource) -> BaseScraper:
        if source == ImageSource.PEXELS:
            return PexelsScraper()
        elif source == ImageSource.PIXABAY:
            return PixabayScraper()
        elif source == ImageSource.UNSPLASH:
            return UnsplashScraper()
        elif source == ImageSource.FIVE_HUNDRED_PX:
            return FiveHundredPxScraper()
        elif source == ImageSource.THIS_PERSON_DOESNOT_EXIST:
            return ThisPersonDoesnotExistScraper()
        else:
            raise Exception(f"Unknown image source: {source.name}")
