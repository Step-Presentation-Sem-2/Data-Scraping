import os
import boto3
import requests
from bs4 import BeautifulSoup as bs
import urllib.request

class scraping_bs():
    '''
    Taking in a url as input and then outputing the images scraped using beautiful soup from each url
    '''
    def __init__(self,base_link):

        self.base_link = base_link
        self.link = '/'.join(base_link.split('/')[:-1])
    
    def get_link(self,img):
        return self.link + '/' + img
    
    def get_image(self, images):
        for img in images:
            try:
                url = img['src'].strip('../')
                img_name = os.path.basename(url)
                link_ = self.get_link(url)
                print(img_name,link_,sep='\t')
                urllib.request.urlretrieve(link_, os.path.join('downloaded_images_umass_1', img_name))
            except:
                continue
            
    def download(self):
        response = requests.get(self.base_link)
        soup = bs(response.text, 'html.parser')
        images = soup.find_all('td')
        os.makedirs('downloaded_images_umass_1', exist_ok=True)

        for img in images:
            next_a_tag = img.find_next('a')
            if next_a_tag and next_a_tag.has_attr('href'):
                img_name = next_a_tag['href']
                link_ = self.get_link(img_name)
                response = requests.get(link_)
                soup = bs(response.text, 'html.parser')
                imgs = soup.find_all('img')
                self.get_image(imgs)

base_link = 'https://vis-www.cs.umass.edu/lfw/alpha_all_1.html'  # Replace with the actual URL
scraper = scraping_bs(base_link)
scraper.download()