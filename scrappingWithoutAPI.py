from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from crawlers.models import Image, Tag, Crawler
from requests.exceptions import HTTPError
import pdb
import signal
import sys
import time

RED = "\033[01;31m{0}\033[00m"
GREEN = "\033[1;36m{0}\033[00m"

def signal_handler(signal, frame):
        global interrupted
        interrupted = True


class Crawler():
    def __init__(self, db_record, origin, base_url, domain):
        """
        current_page is used to track what page the crawler is on

        db_record is an instance of the model class Crawler and represents the associated
        record in the table that keeps track of the crawler in the database

        base_url is the page that is used in order to scrape images from,
        must contain {} where the page number should be

        domain_name is the domain name of the website.
        used to transform relateive urls into absolute urls.
        """
        self.current_page = db_record.current_page
        self.db_record = db_record
        self.origin = origin
        self.base_url = base_url
        self.domain = domain

    def make_absolute_url(self, url):
        """
        returns an absolute url for a given url using the domain_name property
        example: '/photo/bloom-flower-colorful-colourful-9459/' returns 'https://www.pexels.com/photo/bloom-flower-colorful-colourful-9459/'
        where the domain_name is 'www.pexels.com'
        """
        protocol = "https://"
        return urljoin(protocol + self.domain, url)

    def get_page_soup(self, page_url, attempts=5, delay=2):
        for i in range(attempts):
            try:
                response = requests.get(page_url)
                response.raise_for_status()
            except HTTPError as e:
                print (RED.format("page responded with "+str(response.status_code)+". trying again"))
                time.sleep(delay)
            else:
                return BeautifulSoup(response.text)
        else:
            # failed to get the page raise an exception
            response.raise_for_status()

    def get_image_page_urls(self):
        """
        returns a list of urls for each image on the page
        """
        response = requests.get(self.base_url.format(self.current_page))
        page_soup = BeautifulSoup(response.text)

        image_page_urls = [ link['href'] for link in self.get_image_page_links(page_soup)]
        # make sure urls are absolute
        image_page_urls = [self.make_absolute_url(url) for url in image_page_urls]
        return image_page_urls


    def crawl(self):
        global interrupted
        interrupted = False
        signal.signal(signal.SIGINT, signal_handler)
        images_added = 0
        images_failed = 0
        while True:
            print('crawling page {}'.format(self.current_page))
            image_page_urls = self.get_image_page_urls()

            for n,image_page_url in enumerate(image_page_urls):
                if Image.objects.filter(page_url=image_page_url).exists():
                    print("Image already exists in database, moving on")
                    continue
                print('crawling image at: {} (image {} of {})'.format(image_page_url, n+1, len(image_page_urls)))
                try:
                    image_page_soup = self.get_page_soup(image_page_url)
                except HTTPError:
                    print(RED.format("Failed to reach image page url at: {} , moving on".format(image_page_url)))
                    images_failed+=1
                    continue
                print('getting image source url')
                image_source_url = self.get_image_source_url(image_page_soup)
                print('getting image thumbnail url')
                image_thumbnail_url = self.get_image_thumbnail_url(image_page_soup)
                print('getting tags')
                tags = self.get_tags(image_page_soup)
                print('storing image in db')
                self.store_image(image_source_url, image_page_url, image_thumbnail_url, tags)
                images_added+=1

            self.current_page+=1
            self.db_record.current_page+=1
            self.db_record.save()
            if interrupted:
                    print("Crawling halted.")
                    print(GREEN.format("{} images added to database".format(images_added)))
                    print(RED.format("{} images failed to add".format(images_failed)))
                    break

    def get_image_page_links(self, page_soup):
        return NotImplementedError("method get_image_page_links must be implemented")

    def get_image_source_url(self, image_page_soup):
        return NotImplementedError("method get_image_source_url must be implemented")

    def get_image_thumbnail_url(self, image_page_soup):
        return NotImplementedError("method get_image_thumbnail_url must be implemented")

    def get_tags_ul(self, image_page_soup):
        return NotImplementedError("method get_tags_ul must be implemented")



    def get_tags(self, image_page_soup):
        tags_ul = self.get_tags_ul(image_page_soup)
        tag_links = tags_ul.find_all('a')
        tag_names = [tag_link.string for tag_link in tag_links]
        return tag_names

    def store_image(self, image_source_url, image_page_url, image_thumbnail_url, tags):

        image = Image(source_url=image_source_url, page_url=image_page_url, origin=self.origin)

        print('creating thumbnail from url: '+image_thumbnail_url)
        if image.create_thumbnail(image_thumbnail_url):
            print(GREEN.format("thumbnail created"))
        else:
            print(RED.format("thumbnail creation failed, deleting image"))
            image.delete()
            return

        print('saving image')
        image.save()
        print(GREEN.format("new image saved to database"))

        print('adding tags to image')
        for tag in tags:
            tag, created = Tag.objects.get_or_create(name=tag)
            image.tags.add(tag)
            
            
class PexelCrawler(Crawler):
    def __init__(self, db_record=None):
        origin = 'PX'
        base_url = 'https://www.pexels.com/?format=html&page={}'
        domain = 'www.pexels.com'
        Crawler.__init__(self, db_record, origin, base_url, domain)

    def get_image_page_links(self, page_soup):
        article_tags = page_soup.select('article.photos__photo')
        return [article.find('a') for article in article_tags]

    def get_image_source_url(self, image_page_soup):
        return image_page_soup.find('a', class_='js-download')['href']

    def get_image_thumbnail_url(self, image_page_soup):
        return image_page_soup.find('img', class_='photo__img')['src']

    def get_tags_ul(self, image_page_soup):
        return image_page_soup.find('ul', class_='list-padding') 