from image_source import ImageSource
from base_scraper import BaseScraper
from pexels_scraper import PexelsScraper
from pixabay_scraper import PixabayScraper
from unsplash_scraper import UnsplashScraper
from five_hundred_px_scraper import FiveHundredPxScraper


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
        else:
            raise Exception(f"Unknown image source: {source.name}")
